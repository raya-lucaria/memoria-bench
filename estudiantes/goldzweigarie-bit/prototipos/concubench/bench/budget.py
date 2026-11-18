"""Presupuesto de recursos ponderado (memoria + CPU) con admisión FIFO.

Un semáforo por *número* de contenedores no sabe que una tarea pide 2 GB y otra
96 MB: o sobrecomprometes la RAM (OOM del host) o la subutilizas. Aquí cada fase
reserva lo que declara su task.toml y espera hasta que quepa. La admisión es
FIFO estricta: el primero de la fila entra antes que nadie, así una tarea grande
no se queda esperando para siempre detrás de muchas chicas (sin inanición).
"""
from __future__ import annotations

import asyncio
import contextlib
from collections import deque


class Budget:
    def __init__(self, mem_mb: int, cpus: float):
        if mem_mb <= 0 or cpus <= 0:
            raise ValueError("el presupuesto debe ser positivo")
        self.mem_total, self.cpu_total = mem_mb, float(cpus)
        self.mem_free, self.cpu_free = mem_mb, float(cpus)
        self.peak_mem_used = 0
        self.peak_cpu_used = 0.0
        self.max_concurrent = 0
        self._holders = 0
        self._queue: deque[object] = deque()
        self._cv = asyncio.Condition()

    def fits(self, mem_mb: int, cpus: float) -> bool:
        return mem_mb <= self.mem_total and cpus <= self.cpu_total + 1e-9

    async def acquire(self, mem_mb: int, cpus: float) -> None:
        if not self.fits(mem_mb, cpus):
            raise ValueError(
                f"la fase pide {mem_mb} MB / {cpus} CPU y el presupuesto total es "
                f"{self.mem_total} MB / {self.cpu_total} CPU"
            )
        ticket = object()
        async with self._cv:
            self._queue.append(ticket)
            try:
                await self._cv.wait_for(
                    lambda: self._queue[0] is ticket
                    and self.mem_free >= mem_mb
                    and self.cpu_free + 1e-9 >= cpus
                )
            except BaseException:
                self._queue.remove(ticket)
                self._cv.notify_all()
                raise
            self._queue.popleft()
            self.mem_free -= mem_mb
            self.cpu_free -= cpus
            self._holders += 1
            self.peak_mem_used = max(self.peak_mem_used, self.mem_total - self.mem_free)
            self.peak_cpu_used = max(self.peak_cpu_used, self.cpu_total - self.cpu_free)
            self.max_concurrent = max(self.max_concurrent, self._holders)
            self._cv.notify_all()  # el siguiente de la fila puede caber también

    async def release(self, mem_mb: int, cpus: float) -> None:
        async with self._cv:
            self.mem_free += mem_mb
            self.cpu_free += cpus
            self._holders -= 1
            self._cv.notify_all()

    @contextlib.asynccontextmanager
    async def hold(self, mem_mb: int, cpus: float):
        await self.acquire(mem_mb, cpus)
        try:
            yield
        finally:
            await self.release(mem_mb, cpus)

    def stats(self) -> dict:
        return {
            "mem_budget_mb": self.mem_total,
            "cpu_budget": self.cpu_total,
            "peak_mem_reserved_mb": self.peak_mem_used,
            "peak_cpu_reserved": round(self.peak_cpu_used, 2),
            "max_concurrent_phases": self.max_concurrent,
        }

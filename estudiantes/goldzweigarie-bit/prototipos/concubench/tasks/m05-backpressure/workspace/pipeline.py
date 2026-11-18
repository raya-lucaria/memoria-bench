"""Productor–consumidor con hilos.

Uso: python3 pipeline.py params.json
"""
import hashlib
import json
import queue
import sys
import threading

CONSUMERS = 2


def payload(seed: int, i: int, size: int) -> bytes:
    h = hashlib.sha256(f"{seed}:{i}".encode()).digest()
    return h * (size // len(h))


def work(p: bytes, rounds: int) -> bytes:
    d = b""
    for _ in range(rounds):
        d = hashlib.sha256(d + p).digest()
    return d


def main(params_path: str) -> None:
    with open(params_path) as f:
        prm = json.load(f)
    q = queue.Queue()
    results = []
    lock = threading.Lock()

    def producer():
        for i in range(prm["n"]):
            q.put(payload(prm["seed"], i, prm["size"]))
        for _ in range(CONSUMERS):
            q.put(None)

    def consumer():
        acc, count = 0, 0
        while (item := q.get()) is not None:
            d = work(item, prm["rounds"])
            acc ^= int.from_bytes(d[:8], "big")
            count += 1
        with lock:
            results.append((count, acc))

    threads = [threading.Thread(target=producer)] + [threading.Thread(target=consumer) for _ in range(CONSUMERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    total, x = 0, 0
    for c, a in results:
        total += c
        x ^= a
    print(json.dumps({"procesados": total, "xor": f"{x:016x}"}))


if __name__ == "__main__":
    main(sys.argv[1])

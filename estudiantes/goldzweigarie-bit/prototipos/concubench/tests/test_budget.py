import asyncio
import unittest

from bench.budget import Budget


class BudgetTest(unittest.TestCase):
    def test_never_overcommits_and_runs_concurrently(self):
        async def go():
            b = Budget(1000, 4)
            in_use = {"mem": 0, "max": 0}

            async def job(mem, cpu):
                async with b.hold(mem, cpu):
                    in_use["mem"] += mem
                    in_use["max"] = max(in_use["max"], in_use["mem"])
                    await asyncio.sleep(0.01)
                    in_use["mem"] -= mem

            await asyncio.gather(*(job(300, 1) for _ in range(10)))
            return b, in_use

        b, in_use = asyncio.run(go())
        self.assertLessEqual(in_use["max"], 1000)
        self.assertEqual(b.max_concurrent, 3)  # 3 × 300 ≤ 1000 < 4 × 300
        self.assertEqual(b.mem_free, 1000)

    def test_fifo_no_starvation(self):
        """Una fase grande que llega antes no es rebasada por las chicas."""
        async def go():
            b = Budget(1000, 8)
            order = []

            async def job(name, mem, delay):
                await asyncio.sleep(delay)
                async with b.hold(mem, 1):
                    order.append(name)
                    await asyncio.sleep(0.02)

            await asyncio.gather(
                job("chica-1", 600, 0),
                job("grande", 900, 0.001),
                job("chica-2", 100, 0.002),
            )
            return order

        self.assertEqual(asyncio.run(go()), ["chica-1", "grande", "chica-2"])

    def test_rejects_impossible(self):
        async def go():
            await Budget(100, 1).acquire(200, 1)

        with self.assertRaises(ValueError):
            asyncio.run(go())


if __name__ == "__main__":
    unittest.main()

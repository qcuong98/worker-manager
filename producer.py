import asyncio
import random

class Producer:
    def __init__(self, name, loop):
        self.name = name
        self.loop = loop
        self.queue = asyncio.Queue()
        self.coro_task = self.loop.create_task(self.produce())

    async def produce(self):
        pass
        # for i in range(5):
        #     difficulty = random.randint(1, 5)
        #     await asyncio.sleep(random.random())
        #     print(f"[Task {self.name}] Generating a item has difficulty = {difficulty}")
        #     await self.queue.put(difficulty)
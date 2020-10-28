import asyncio
import uuid
from abc import ABC

WORKER_STATUS = {
    'WAITING': 0,
    'EXECUTING': 1,
    'STOPPED': 2
}

class Worker(ABC):
    def __init__(self, producers, loop):
        self.id = uuid.uuid4()
        self.type = ""
        self.producers = producers
        self.loop = loop
        self.execution_speed = 1
        self.status = WORKER_STATUS['WAITING']
        self.coro_task = self.loop.create_task(self.excute())

        self.done = asyncio.Event()
        self.done.set()

    async def excute(self):
        while True:
            for producer in self.producers:
                # wait for an item from the producer
                try:
                    difficulty = producer.queue.get_nowait()
                except asyncio.QueueEmpty:
                    continue

                # excute the task
                self.status = WORKER_STATUS['EXECUTING']
                self.done.clear()
                await asyncio.sleep(difficulty / self.execution_speed)
                self.status = WORKER_STATUS['WAITING']
                self.done.set()

            await asyncio.sleep(0.1)

    async def shutdown(self):
        await self.done.wait()
        self.coro_task.cancel()
        self.status = WORKER_STATUS['STOPPED']

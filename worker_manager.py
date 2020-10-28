import asyncio
from workerA import WorkerA
from workerB import WorkerB
from workerC import WorkerC
from producer import Producer

STATUS = ['WAITING', 'EXECUTING', 'STOPPED']

class WorkerManager:
    def __init__(self):
        pass

    async def main(self):
        self.loop = asyncio.get_event_loop()
        self.job_1 = Producer("Business", self.loop)
        self.job_2 = Producer("Technical", self.loop)

        self.workers = [
            WorkerA([self.job_1, self.job_2], self.loop) for _ in range(4)
        ]
        self.workers += [WorkerB([self.job_1], self.loop) for _ in range(7)]
        self.workers += [WorkerC([self.job_2], self.loop) for _ in range(2)]

        await self.job_1.coro_task
        await self.job_2.coro_task
        for worker in self.workers:
            await worker.coro_task

    def add_task(self, task, difficulty):
        if task == "Business":
            self.loop.call_soon_threadsafe(self.job_1.queue.put_nowait,
                                           difficulty)
        else:
            self.loop.call_soon_threadsafe(self.job_2.queue.put_nowait,
                                           difficulty)

    def get_worker_status(self):
        l = []
        for worker in self.workers:
            l.append({
                "type": worker.type,
                "id": worker.id,
                "status": STATUS[worker.status]
            })
        return l

    def shutdown_worker(self, worker_id):
        for worker in self.workers:
            if worker.id == worker_id:
                asyncio.run(worker.shutdown())
                worker.waiting_for_shutdown = True

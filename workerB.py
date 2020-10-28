from worker import Worker

class WorkerB(Worker):
    def __init__(self, producers, loop):
        super().__init__(producers, loop)
        self.execution_speed = 1.2
        self.type = "B"

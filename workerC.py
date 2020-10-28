from worker import Worker

class WorkerC(Worker):
    def __init__(self, producers, loop):
        super().__init__(producers, loop)
        self.execution_speed = 1.0
        self.type = "C"

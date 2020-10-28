from worker import Worker

class WorkerA(Worker):
    def __init__(self, producers, loop):
        super().__init__(producers, loop)
        self.execution_speed = 1.5
        self.type = "A"
    

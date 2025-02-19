class FailedOnGetJob(Exception):
    def __init__(self):
        self.message = "Failed on get your job!"
        super().__init__(self.message)
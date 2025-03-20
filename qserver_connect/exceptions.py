class FailedOnGetJobResult(Exception):
    def __init__(self):
        super().__init__("Failed on get your job resuts!")

class FailedOnGetJobData(Exception):
    def __init__(self):
        super().__init__("Failed on get your job data!")

class JobNotFound(Exception):
    def __init__(self, job_id:str):
        super().__init__(f"Job not found with id: {job_id}")

class FailedOnAddPlugin(Exception):
    def __init__(self, plugin_name:str):
        super().__init__(f"Failed on Add Plugin: {plugin_name}")

class FailedOnDeletePlugin(Exception):
    def __init__(self, plugin_name:str):
        super().__init__(f"Failed on Delete Plugin: {plugin_name}")
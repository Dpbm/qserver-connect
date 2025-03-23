from typing import Any
from abc import ABC, abstractmethod
from ..data_types import CreateJobData
from ..job import Job
from ..job_connection import JobConnection


class Adapter(ABC, JobConnection):
    """
    An abstract class to make a contract to what a adapter
    needs to have to work properly.
    """

    @abstractmethod
    def create_job(self, qc: Any, data: CreateJobData) -> Job:
        """
        Abstract method to encapsulate a job into a object.
        """

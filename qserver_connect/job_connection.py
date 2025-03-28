import json
import logging
from http import HTTPStatus
import requests as req
import grpc  # type: ignore
from .url import URL, HTTP
from .data_types import (
    Response,
    JobId,
    AllData,
)
from .exceptions import FailedOnGetJobResult, FailedOnGetJobData, JobNotFound
from .constants import TIMEOUT_TIME
from .job import Job
from .jobs_pb2 import JobData, JobProperties  # pylint: disable=no-name-in-module
from .jobs_pb2_grpc import JobsStub

logger = logging.getLogger(__name__)


class Data:
    """
    An iterator for streaming job data through grpc.
    """

    def __init__(self, all_data: AllData):
        """
        Setup data and first batch to be sent.
        """
        self._iteration = 0
        self._qasm_path = all_data["qasm"]
        self._first_batch = Data.prepare_first_batch(all_data)

    @staticmethod
    def prepare_first_batch(data: AllData) -> JobData:
        """
        Get all the data that can be passed in a single batch before sending the qasm
        code.
        """

        return JobData(
            properties=JobProperties(
                resultTypeCounts=data["counts"],
                resultTypeQuasiDist=data["quasi_dist"],
                resultTypeExpVal=data["expval"],
                targetSimulator=data["simulator"],
                metadata=json.dumps(data["metadata"]),
            )
        )

    def get_chunk(self) -> str:
        """
        Open qasm file and get a chunck of 16kb.
        """

        chunck_size = 16 * 1024  # 16Kb
        file_pos = (self._iteration - 1) * chunck_size

        with open(self._qasm_path, "r", encoding="utf-8") as file:
            file.seek(file_pos)
            return file.read(chunck_size)

    def __next__(self):
        """
        Get qasm batch.
        """

        batch = self._first_batch

        if self._iteration > 0:
            chunk = self.get_chunk()

            if not chunk:
                raise StopIteration

            batch = JobData(qasmChunk=chunk)

        self._iteration += 1

        return batch


class JobConnection:
    """
    HTTP and GRPC connection class to interact with jobs.
    """

    def __init__(
        self, host: str, http_port: int, grpc_port: int, secure_connection: bool = True
    ):
        """
        Setup HTTP and GRPC handlers.
        """
        self._host = host
        self._http_port = http_port
        self._grpc_port = grpc_port
        self._secure = secure_connection
        self._http_handler = URL(host, http_port, http=HTTP(secure_connection))
        self._grpc_handler = URL(host, grpc_port, http=HTTP(secure_connection))

    def send_job(self, job_data: Job) -> JobId:
        """
        Stream job data through GRPC.
        """

        logger.debug("adding job")
        url = self._grpc_handler.get_add_job_url()
        logger.debug("using url: %s", url)

        # pylint: disable=fixme
        # TODO: add secure channel
        with grpc.insecure_channel(url, compression=grpc.Compression.Gzip) as channel:

            stub = JobsStub(channel)

            data = job_data.data
            logger.debug("Sending data: %s", data)
            # once the grpc server checks the data an raise an error when
            # it doesn't match with the schema, we don't need to recheck the data here
            job = stub.AddJob(Data(data))
            job_id = str(job.id)
            logger.debug("Got job id: %s", job_id)

            return job_id

    def get_job_data(self, job_id: str) -> Response:
        """
        Get data releative to the provided job_id.
        """

        logger.debug("getting job data: %s", job_id)
        url = self._http_handler.get_job_data_url(job_id)
        logger.debug("using url: %s", url)

        json_data = {}
        response_status = int(HTTPStatus.BAD_REQUEST)

        try:
            response_data = req.get(url, timeout=TIMEOUT_TIME)
            json_data = response_data.json()
            response_status = response_data.status_code

        except Exception as error:
            logger.error("Failed on get job data: %s")
            logger.error(str(error))
            raise FailedOnGetJobData() from error

        if response_status == HTTPStatus.NOT_FOUND:
            raise JobNotFound(job_id)
        if len(json_data) <= 0 or response_status != HTTPStatus.OK:
            raise FailedOnGetJobData()

        return json_data

    def get_job_result(self, job_id: str) -> Response:
        """
        Get results from your job.
        """

        logger.debug("getting job result: %s", job_id)
        url = self._http_handler.get_job_result_url(job_id)
        logger.debug("using url: %s", url)

        json_data = {}
        response_status = int(HTTPStatus.BAD_REQUEST)

        try:
            response_data = req.get(url, timeout=TIMEOUT_TIME)
            json_data = response_data.json()
            response_status = response_data.status_code

        except Exception as error:
            logger.error("Failed on get job results data")
            logger.error(str(error))
            raise FailedOnGetJobResult() from error

        if response_status == HTTPStatus.NOT_FOUND:
            raise JobNotFound(job_id)
        if len(json_data) <= 0 or response_status != HTTPStatus.OK:
            raise FailedOnGetJobResult()

        return json_data

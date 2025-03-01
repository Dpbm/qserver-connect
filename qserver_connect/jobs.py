import requests as req

import grpc
import json

from .utils import get_url
from .data_types import (
    Response, 
    Metadata, 
    QasmPath, 
    UseCounts, 
    UseExpval, 
    UseQuasiDist, 
    Simulator, 
    JobId, 
    AllData
)
from .exceptions import FailedOnGetJob

from .jobs_pb2 import JobData,JobProperties
from .jobs_pb2_grpc import JobsStub


class Data:
    def __init__(self, all_data:AllData):
        self._iteration = 0
        self._qasm_path = all_data['qasm']
        self._first_batch = self.prepare_first_batch(all_data)

    @staticmethod
    def prepare_first_batch(data:AllData) -> JobData:
        """
            Get all the data that can be passed in a single batch before sending the qasm 
            code.
        """

        return JobData(properties=JobProperties(
            resultTypeCounts=data['counts'],
            resultTypeQuasiDist=data['quasi_dist'],
            resultTypeExpVal=data['expval'],
            targetSimulator=data['simulator'],
            metadata=json.dumps(data['metadata'])
        ))
        

    def get_chunk(self) -> str:
        chunck_size = 16 * 1024 #16Kb
        file_pos = (self._iteration-1) * chunck_size

        with open(self._qasm_path, "r", encoding="utf-8") as file:
            file.seek(file_pos)
            return file.read(chunck_size)

    def __next__(self):
        batch = self._first_batch

        if(self._iteration > 0):
            chunk = self.get_chunk()

            if not chunk:
                raise StopIteration

            batch = JobData(qasmChunk=chunk)
        
        self._iteration += 1

        return batch

class Jobs:
    def __init__(self, host:str, port:int):
        self._host = host
        self._port = port
        self._full_url = f"{host}:{port}"

    def send_job(self, 
        qasm_path:QasmPath, 
        get_counts:UseCounts, 
        get_quasi_dist:UseQuasiDist, 
        get_expval:UseExpval, 
        target_simualtor:Simulator, 
        metadata:Metadata = {}) -> JobId:

        with grpc.insecure_channel(
                get_url(self._full_url, "add"), 
                compression=grpc.Compression.Gzip) as channel:

            stub = JobsStub(channel)

            all_data = {
                "qasm": qasm_path,
                "counts": get_counts,
                "quasi_dist": get_quasi_dist,
                "expval": get_expval,
                "simulator":target_simualtor,
                "metadata":metadata
            }

            job = stub.AddJob(Data(all_data))
            return job.id


    def get_job(self, job_id:str) -> Response:
        response_data = req.get(get_url(self._full_url, "get", job_id))
        json_data = response_data.json()

        if(response_data.status_code != 200 or len(json_data.items()) <= 0):
            raise FailedOnGetJob()

        return json_data
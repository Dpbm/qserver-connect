import requests as req
from typing import Dict, Any

from .utils import get_url
from .exceptions import FailedOnGetJob

Response = Dict[str, Any]


class Jobs:
    def __init__(self, host:str, port:int):
        self._host = host
        self._port = port
        self._full_url = f"http://{host}:{str(port)}" 

    def send_job(self):
        raise NotImplementedError

    def get_job(self, job_id:str) -> Response:
        response_data = req.get(get_url(self._full_url, "get", job_id))
        json_data = response_data.json()

        if(response_data.status_code != 200 or len(json_data.items()) <= 0):
            raise FailedOnGetJob()

        return json_data
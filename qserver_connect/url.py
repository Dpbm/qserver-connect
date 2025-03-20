from typing import Optional

class HTTP:
    def __init__(self, secure:bool=True):
        self._secure = secure

    def get_protocol(self) -> str:
        return 'https' if self._secure else 'http'

class URL:
    def __init__(self, host:str, port:int, http:HTTP=HTTP()):
        self._host = host
        self._port = port

        self._url = f'{host}:{str(port)}'
        self._http = http

    def get_job_result_url(self, job_id:str) -> str:
        return f'{self._http.get_protocol()}://{self._url}/api/v1/job/result/{job_id}'

    def get_job_data_url(self, job_id:str) -> str:
        return f'{self._http.get_protocol()}://{self._url}/api/v1/job/{job_id}'

    def get_add_job_url(self) -> str:
        return f'{self._url}/'

    def get_add_plugin_url(self, name:str) -> str:
        return f'{self._http.get_protocol()}://{self._url}/api/v1/plugin/{name}'

    def get_delete_plugin_url(self, name:str) -> str:
        return self.get_add_plugin_url(name)


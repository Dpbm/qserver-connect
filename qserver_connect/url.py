class HTTP:
    """
    It handles data about HTTP connections.
    """

    def __init__(self, secure: bool = True):
        """
        Initilize http connection data.
        """
        self._secure = secure

    def get_protocol(self) -> str:
        """
        Check if we should use http or https
        """

        return "https" if self._secure else "http"


class URL:
    """
    Class in charge of mapping routes based on backend urls.
    """

    def __init__(self, host: str, port: int, http: HTTP = HTTP()):
        """
        Setup connections for HTTP and GRPC.
        """

        self._host = host
        self._port = port

        self._url = f"{host}:{str(port)}"
        self._http = http

    def get_job_result_url(self, job_id: str) -> str:
        """
        Get the route which returns the results of a job.
        """
        return f"{self._http.get_protocol()}://{self._url}/api/v1/job/result/{job_id}"

    def get_job_data_url(self, job_id: str) -> str:
        """
        Get the route which returns the data of a job.
        """
        return f"{self._http.get_protocol()}://{self._url}/api/v1/job/{job_id}"

    def get_add_job_url(self) -> str:
        """
        Get for grpc connection, meant to be used for adding jobs.
        """
        return f"{self._url}/"

    def get_add_plugin_url(self, name: str) -> str:
        """
        Returns the url for the route which is used to add plugins.
        """
        return f"{self._http.get_protocol()}://{self._url}/api/v1/plugin/{name}"

    def get_delete_plugin_url(self, name: str) -> str:
        """
        Returns the url for the route which is used to remove plugins.
        """
        return self.get_add_plugin_url(name)

from time import sleep
import pytest
from qserver_connect import JobConnection, Plugin
from qserver_connect.exceptions import FailedOnGetJobData, FailedOnGetJobResult


class TestJobs:
    """
    Test suite for jobs actions.
    """

    def test_result_invalid_id(self, connection):
        """should raise an error once the id is invalid"""

        host, port_http, port_grpc = connection

        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        with pytest.raises(FailedOnGetJobResult):
            j.get_job_result("AAAA")

    def test_result_valid_id(self, connection, plugin_name, short_job_data):
        """should return successfully the results from job"""

        host, port_http, port_grpc = connection

        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(plugin_name)

        job_id = j.send_job(short_job_data)

        job_status = "pending"
        while job_status in ["pending", "running"]:
            sleep(2)
            data = j.get_job_data(job_id)
            job_status = data["status"]

        if job_status == "failed":
            pytest.fail()

        j.get_job_result(job_id)

    def test_get_job_data_invalid_id(self, connection):
        """should failed on get job data once the id is invalid"""
        host, port_http, port_grpc = connection
        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        with pytest.raises(FailedOnGetJobData):
            j.get_job_data("AAAA")

    def test_get_job_data_successfully(self, connection, plugin_name, short_job_data):
        """should return successfully the data from job"""

        host, port_http, port_grpc = connection

        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(plugin_name)

        job_id = j.send_job(short_job_data)

        j.get_job_data(job_id)

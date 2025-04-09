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

    def test_result_valid_id(self, connection, plugin_name, job_data):
        """should return successfully the results from job"""

        host, port_http, port_grpc = connection

        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(plugin_name)

        job_id = j.send_job(job_data)

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

    def test_get_job_data_successfully(self, connection, plugin_name, job_data):
        """should return successfully the data from job"""

        host, port_http, port_grpc = connection

        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(plugin_name)

        job_id = j.send_job(job_data)

        j.get_job_data(job_id)

    def test_get_all_jobs_with_no_jobs(self, connection):
        """should return an empty array"""
        host, port_http, port_grpc = connection
        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )

        jobs = j.get_all_jobs()

        assert len(jobs) == 0

    def test_get_all_jobs_with_two_jobs(self, connection, plugin_name, job_data):
        """should return an array with 2 jobs"""

        host, port_http, port_grpc = connection
        j = JobConnection(
            host=host,
            http_port=port_http,
            grpc_port=port_grpc,
            secure_connection=False,
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(plugin_name)

        j.send_job(job_data)
        j.send_job(job_data)

        jobs = j.get_all_jobs()

        assert len(jobs) == 2

    def test_delete_job(self, connection, plugin_name, job_data):
        """should delete a job with no errors"""

        host, port_http, port_grpc = connection

        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(plugin_name)

        job_id = j.send_job(job_data)

        job_status = "pending"
        while job_status in ["pending", "running"]:
            sleep(2)
            data = j.get_job_data(job_id)
            job_status = data["status"]

        if job_status == "failed":
            pytest.fail()

        j.delete_job(job_id)

    def test_https(self, connection_secure, plugin_name, job_data):
        """should add a job with no connection problems"""

        host, port_https, port_grpc = connection_secure

        j = JobConnection(
            host=host, http_port=port_https, grpc_port=port_grpc, secure_connection=True
        )
        p = Plugin(host=host, port=port_https, secure_connection=True)

        p.add_plugin(plugin_name)

        job_id = j.send_job(job_data)

        job_status = "pending"
        while job_status in ["pending", "running"]:
            sleep(2)
            data = j.get_job_data(job_id)
            job_status = data["status"]

        if job_status == "failed":
            pytest.fail()

        j.delete_job(job_id)

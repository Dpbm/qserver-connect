import pytest
import os
from time import sleep
from qserver_connect import Jobs, Plugin
from qserver_connect.exceptions import FailedOnGetJobData, FailedOnGetJobResult

DEFAULT_PLUGIN = "aer-plugin"
host = os.getenv("HOST")
port_http = int(os.getenv("PORT_HTTP"))
port_grpc = int(os.getenv("PORT_GRPC"))


@pytest.fixture(autouse=True)
def delete_default_plugin():
    p = Plugin(host=host, port=port_http, secure_connection=False)

    try:
        p.delete_plugin(DEFAULT_PLUGIN)
    except Exception as error:
        print("Failed on delete plugin")
        print(str(error))


class TestJobs:
    def test_result_invalid_id(self):
        j = Jobs(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        with pytest.raises(FailedOnGetJobResult):
            j.get_job_result("AAAA")

    def test_result_valid_id(self):
        j = Jobs(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        p = Plugin(host=host, port=port_http, secure_connection=False)

        p.add_plugin(DEFAULT_PLUGIN)

        job_id = j.send_job(
            qasm_path="./tests/test.qasm",
            get_counts=True,
            get_expval=False,
            get_quasi_dist=False,
            target_simualtor="aer",
        )

        job_status = "pending"
        while job_status in ["pending", "running"]:
            sleep(2)
            data = j.get_job_data(job_id)
            job_status = data["status"]

        if job_status == "failed":
            pytest.fail()

        j.get_job_result(job_id)

    def test_get_job_data_invalid_id(self):
        j = Jobs(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )
        with pytest.raises(FailedOnGetJobData):
            j.get_job_data("AAAA")

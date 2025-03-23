import pytest
import os
from qserver_connect import Jobs, Plugin
from qserver_connect.exceptions import (
    FailedOnGetJobData,
    FailedOnGetJobResult,
    FailedOnDeletePlugin,
)


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


class TestPlugins:
    def test_add_plugin(self):

        p = Plugin(host=host, port=port_http, secure_connection=False)
        p.add_plugin(DEFAULT_PLUGIN)

    def test_remove_plugin(self):
        p = Plugin(host=host, port=port_http, secure_connection=False)
        p.add_plugin(DEFAULT_PLUGIN)
        p.delete_plugin(DEFAULT_PLUGIN)

    def test_delete_plugin_when_job_is_running(self):
        p = Plugin(host=host, port=port_http, secure_connection=False)
        j = Jobs(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )

        p.add_plugin(DEFAULT_PLUGIN)

        job_id = j.send_job(
            qasm_path="./tests/test.qasm",
            get_counts=True,
            get_expval=False,
            get_quasi_dist=False,
            target_simualtor="aer",
        )

        p.delete_plugin(DEFAULT_PLUGIN)

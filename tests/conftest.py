import os
import pytest
from qserver_connect import Plugin
from qserver_connect.job import Job


@pytest.fixture
def connection():
    """
    get variables related to the connection with the backend
    """

    host = os.getenv("HOST")
    port_http = int(os.getenv("PORT_HTTP"))
    port_grpc = int(os.getenv("PORT_GRPC"))

    return (host, port_http, port_grpc)


@pytest.fixture
def backend() -> str:
    """
    get backend name
    """
    return "aer"


@pytest.fixture
def plugin_name() -> str:
    """
    get the plugin name
    """

    return "aer-plugin"


@pytest.fixture
# pylint: disable=redefined-outer-name
def long_job_data(backend:str) -> Job:
    """
    job data for a time consuming task
    """

    return Job({
        "qasm": "./tests/test_big_circuit.qasm",
        "counts": True,
        "expval": False,
        "quasi_dist": False,
        "simulator": backend,
        "metadata": {},
    })


@pytest.fixture
# pylint: disable=redefined-outer-name
def short_job_data(backend:str) -> Job:
    """
    job data for a low time consuming task
    """

    return Job({
        "qasm": "./tests/test.qasm",
        "counts": True,
        "expval": False,
        "quasi_dist": False,
        "simulator": backend,
        "metadata": {},
    })


@pytest.fixture(autouse=True)
# pylint: disable=redefined-outer-name
def delete_default_plugin(connection, plugin_name):
    """
    Delete plugins from database before running each test
    """

    host, port_http, _ = connection

    p = Plugin(host=host, port=port_http, secure_connection=False)

    try:
        p.delete_plugin(plugin_name)

    except Exception as error:
        print("Failed on delete plugin")
        print(str(error))

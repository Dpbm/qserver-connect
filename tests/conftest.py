import os
from time import sleep
import pytest
from qserver_connect import Plugin, JobConnection
from qserver_connect.job import Job


@pytest.fixture
def connection():
    """
    get variables related to the connection with the backend
    """

    host = os.getenv("HOST")
    port_http = 8080
    port_grpc = 8080

    return (host, port_http, port_grpc)


@pytest.fixture
def connection_secure():
    """
    get variables related to the connection with the backend using tls
    """

    host = os.getenv("HOST")
    port_http = 443
    port_grpc = 443

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
def job_data(backend: str) -> Job:
    """
    job data for a low time consuming task
    """

    return Job(
        {
            "qasm": "./tests/test.qasm",
            "counts": True,
            "expval": False,
            "quasi_dist": False,
            "simulator": backend,
            "metadata": {},
        }
    )


@pytest.fixture(autouse=True)
# pylint: disable=redefined-outer-name
def delete_default_plugin(connection, plugin_name):
    """
    Delete plugins from database before running each test.
    It must check for jobs and delete them as well.
    """
    host, port_http, port_grpc = connection

    j = JobConnection(
        grpc_port=port_grpc, host=host, http_port=port_http, secure_connection=False
    )
    p = Plugin(host=host, port=port_http, secure_connection=False)

    jobs = j.get_all_jobs()

    # the following code is meant to fail. Don't do any exception handling here.
    # If you can't stop the jobs, you already have a problem.

    all_jobs_ids = [job["id"] for job in jobs]
    running_jobs = [job["id"] for job in jobs if job["status"] == "running"]
    if len(jobs) > 0 and len(running_jobs) > 0:
        print("There're jobs running")

        while len(running_jobs) != 0:

            new_jobs_statuses = []

            for job_id in running_jobs:
                data = j.get_job_data(job_id)

                if data["status"] == "running":
                    new_jobs_statuses.append(data["id"])

            running_jobs = new_jobs_statuses
            sleep(2)

    for job_id in all_jobs_ids:
        j.delete_job(job_id)

    try:
        p.delete_plugin(plugin_name)

    except Exception as error:
        print("Failed on delete plugin")
        print(str(error))

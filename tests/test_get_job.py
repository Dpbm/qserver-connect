import pytest
import os
import requests as req

from qserver_connect import Jobs
from qserver_connect.exceptions import FailedOnGetJob


DEFAULT_PLUGIN = 'aer-plugin'
host = os.getenv("HOST")
port = int(os.getenv("PORT")) 

class TestGetJob:
    def test_invalid_id(self):
        j = Jobs(host=host, port=port)
        
        with pytest.raises(FailedOnGetJob):
            j.get_job("AAAA")

    def test_valid_id(self):
        j = Jobs(host=host, port=port)

        req.post(f'http://{host}:{port}/api/plugin/{DEFAULT_PLUGIN}')

        id = j.send_job(
            qasm_path="./tests/test.qasm",
            get_counts=True,
            get_expval=False,
            get_quasi_dist=False,
            target_simualtor="aer"
        )
        j.get_job(id)

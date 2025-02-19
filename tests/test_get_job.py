import pytest
import os

from qserver_connect import Jobs
from qserver_connect.exceptions import FailedOnGetJob

host = os.getenv("HOST")
port = int(os.getenv("PORT")) 

class TestGetJob:
    def test_invalid_id(self):
        j = Jobs(host=host, port=port)
        
        with pytest.raises(FailedOnGetJob):
            j.get_job("AAAA")

    def test_valid_id(self):
        j = Jobs(host=host, port=port)

        id = j.send_job()
        j.get_job(id)

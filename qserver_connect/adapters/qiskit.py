from typing import Any
import logging
import os
import tempfile
import uuid

from ..exceptions import (
    InvalidObservables,
    FailedOnCreateJob,
    InvalidResultTypes,
    QiskitError,
)

try:
    from qiskit import qasm3
except ImportError as error:
    raise QiskitError() from error

from ..data_types import CreateJobData, Metadata
from ..job import Job
from .adapter import Adapter

logger = logging.getLogger(__name__)


class Qiskit(Adapter):
    """
    An Adapter to Qiskit. It's meant to ease the process of managing
    jobs with the IBM quantum framework.
    """

    def __init__(
        self, host: str, http_port: int, grpc_port: int, secure_connection: bool = True
    ):
        """
        Setup data.
        """

        super().__init__(host, http_port, grpc_port, secure_connection)
        self._job = None

    def create_job(self, qc: Any, data: CreateJobData) -> Job:
        """
        Method to retrieve all data necessary to run the job from a qiskit QuantumCircuit object.
        """

        expval = data["expval"]
        counts = data["counts"]
        quasi_dist = data["quasi_dist"]
        obs = data["obs"]
        shots = data["shots"]

        if not any([counts, quasi_dist, expval]):
            raise InvalidResultTypes()

        if expval and obs is None:
            raise InvalidObservables()

        metadata: Metadata = {}

        if expval:
            metadata["obs"] = obs

        if (counts or quasi_dist) and shots is not None:
            metadata["shots"] = shots

        with tempfile.TemporaryDirectory(delete=False) as tempdir:

            try:

                logger.debug("exporting qc to qasm3...")

                filename = f"{str(uuid.uuid4())}.qasm"
                qasm_path = os.path.join(tempdir.name, filename)  # type:ignore
                logger.debug("file will be exported to: %s", qasm_path)
                qasm3.dump(qc, qasm_path)

                logger.debug("filed exported successfully")
                logger.debug("job created successfully")

                return Job(
                    {
                        "simulator": data["backend"],
                        "counts": counts,
                        "expval": expval,
                        "quasi_dist": quasi_dist,
                        "metadata": metadata,
                        "qasm": qasm_path,
                    }
                )

            except Exception as error:
                logger.error("Failed on create job")
                logger.error(str(error))
                raise FailedOnCreateJob() from error

from typing import Any
import logging
import tempfile
from ..exceptions import (
    InvalidObservables,
    FailedOnCreateJob,
    InvalidResultTypes,
    QiskitError,
)

try:
    from qiskit import qasm2
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

        with tempfile.NamedTemporaryFile(
            delete_on_close=False, delete=False, suffix=".qasm"
        ) as temp_qasm_file:

            try:

                logger.debug("exporting qc to qasm3...")
                qasm_path = temp_qasm_file.name
                logger.debug("file will be exported to: %s", qasm_path)

                with open(qasm_path, "w", encoding="utf-8") as qasm_file:
                    qasm2.dump(qc, qasm_file)

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

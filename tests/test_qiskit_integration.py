import os
import pytest
from qiskit import QuantumCircuit
from qserver_connect import Qiskit
from qserver_connect.exceptions import InvalidResultTypes, InvalidObservables


class TestQiskit:
    """
    Test qiskit Adapter.
    """

    def test_failed_create_job_invalid_result_types(self, connection, backend):
        """should raise an error due to the invalid result types"""
        host, port_http, port_grpc = connection

        q = Qiskit(host, port_http, port_grpc)

        qc = QuantumCircuit(1)

        with pytest.raises(InvalidResultTypes):
            q.create_job(
                qc,
                {
                    "backend": backend,
                    "counts": False,
                    "quasi_dist": False,
                    "expval": False,
                    "shots": None,
                    "obs": None,
                },
            )

    def test_failed_create_job_no_observables(self, connection, backend):
        """should raise an error due to the lack of observables for expval extraction"""
        host, port_http, port_grpc = connection

        q = Qiskit(host, port_http, port_grpc)

        qc = QuantumCircuit(1)

        with pytest.raises(InvalidObservables):
            q.create_job(
                qc,
                {
                    "backend": backend,
                    "counts": True,
                    "quasi_dist": False,
                    "expval": True,
                    "shots": None,
                    "obs": None,
                },
            )

    def test_metadata_expval(self, connection, backend):
        """should return a job with an observables in its metadata"""
        host, port_http, port_grpc = connection

        q = Qiskit(host, port_http, port_grpc)

        qc = QuantumCircuit(1)

        job = q.create_job(
            qc,
            {
                "backend": backend,
                "counts": False,
                "quasi_dist": False,
                "expval": True,
                "shots": None,
                "obs": [[("XX", 1)]],
            },
        )

        data = job.data

        assert data["simulator"] == backend
        assert data["counts"] is False
        assert data["quasi_dist"] is False
        assert data["expval"] is True
        assert data["metadata"] == {"obs": [[("XX", 1)]]}
        assert os.path.exists(data["qasm"]) is True

    def test_get_counts_without_shots(self, connection, backend):
        """should return a job with no problems, once a shots has a default value"""
        host, port_http, port_grpc = connection

        q = Qiskit(host, port_http, port_grpc)

        qc = QuantumCircuit(1)

        job = q.create_job(
            qc,
            {
                "backend": backend,
                "counts": True,
                "quasi_dist": False,
                "expval": False,
                "shots": None,
                "obs": None,
            },
        )

        data = job.data

        assert data["simulator"] == backend
        assert data["counts"] is True
        assert data["quasi_dist"] is False
        assert data["expval"] is False
        assert data["metadata"] == {}
        assert os.path.exists(data["qasm"]) is True

    def test_get_counts_with_shots(self, connection, backend):
        """should return a job with shots set in its metadata"""
        host, port_http, port_grpc = connection

        q = Qiskit(host, port_http, port_grpc)

        qc = QuantumCircuit(1)

        job = q.create_job(
            qc,
            {
                "backend": backend,
                "counts": True,
                "quasi_dist": False,
                "expval": False,
                "shots": 120,
                "obs": None,
            },
        )

        data = job.data

        assert data["simulator"] == backend
        assert data["counts"] is True
        assert data["quasi_dist"] is False
        assert data["expval"] is False
        assert data["metadata"] == {"shots": 120}
        assert os.path.exists(data["qasm"]) is True

    def test_qasm_file(self, connection, backend):
        """should create a correct temp qasm file"""
        host, port_http, port_grpc = connection

        q = Qiskit(host, port_http, port_grpc)

        total_qubits = 3
        qc = QuantumCircuit(total_qubits)

        job = q.create_job(
            qc,
            {
                "backend": backend,
                "counts": True,
                "quasi_dist": False,
                "expval": False,
                "shots": None,
                "obs": None,
            },
        )

        qasm_path = job.data["qasm"]

        assert os.path.exists(qasm_path) is True

        qasm_qc = QuantumCircuit.from_qasm_file(qasm_path)

        assert qasm_qc.num_qubits == total_qubits
        assert qasm_qc.depth() == 0

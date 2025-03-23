from typing import Dict, Any, TypedDict, Tuple, List, Optional

Response = Dict[str, Any]
Metadata = Dict[str, Any]
QasmPath = str
UseCounts = bool
UseQuasiDist = bool
UseExpval = bool
Simulator = str
JobId = str
Observables = List[List[Tuple[str, float]]]
Shots = int


class AllData(TypedDict):
    """
    A type for the job expected data input.
    """

    qasm: QasmPath
    counts: UseCounts
    quasi_dist: UseQuasiDist
    expval: UseExpval
    simulator: Simulator
    metadata: Metadata


class CreateJobData(TypedDict):
    """
    A type for creating job.
    """

    backend: Simulator
    counts: UseCounts
    quasi_dist: UseQuasiDist
    expval: UseExpval
    shots: Optional[Shots]
    obs: Optional[Observables]

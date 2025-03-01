from typing import Dict, Any, TypedDict

Response = Dict[str, Any]
Metadata = Dict[Any, Any]
QasmPath = str
UseCounts = bool
UseQuasiDist = bool
UseExpval = bool
Simulator = str
JobId = str


class AllData(TypedDict):
    qasm:QasmPath 
    counts:UseCounts 
    quasi_dist:UseQuasiDist 
    expval:UseExpval
    simulator:Simulator
    metadata:Metadata

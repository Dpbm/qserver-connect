from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class JobProperties(_message.Message):
    __slots__ = (
        "resultTypeCounts",
        "resultTypeQuasiDist",
        "resultTypeExpVal",
        "targetSimulator",
        "metadata",
    )
    RESULTTYPECOUNTS_FIELD_NUMBER: _ClassVar[int]
    RESULTTYPEQUASIDIST_FIELD_NUMBER: _ClassVar[int]
    RESULTTYPEEXPVAL_FIELD_NUMBER: _ClassVar[int]
    TARGETSIMULATOR_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    resultTypeCounts: bool
    resultTypeQuasiDist: bool
    resultTypeExpVal: bool
    targetSimulator: str
    metadata: str
    def __init__(
        self,
        resultTypeCounts: bool = ...,
        resultTypeQuasiDist: bool = ...,
        resultTypeExpVal: bool = ...,
        targetSimulator: _Optional[str] = ...,
        metadata: _Optional[str] = ...,
    ) -> None: ...

class JobData(_message.Message):
    __slots__ = ("properties", "qasmChunk")
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    QASMCHUNK_FIELD_NUMBER: _ClassVar[int]
    properties: JobProperties
    qasmChunk: str
    def __init__(
        self,
        properties: _Optional[_Union[JobProperties, _Mapping]] = ...,
        qasmChunk: _Optional[str] = ...,
    ) -> None: ...

class PendingJob(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class HealthCheckInput(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Health(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

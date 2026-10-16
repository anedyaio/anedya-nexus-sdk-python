from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmitDataRequest(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[NodeData]
    def __init__(self, data: _Optional[_Iterable[_Union[NodeData, _Mapping]]] = ...) -> None: ...

class NodeData(_message.Message):
    __slots__ = ("node_id", "datapoints")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    datapoints: _containers.RepeatedCompositeFieldContainer[VariableData]
    def __init__(self, node_id: _Optional[str] = ..., datapoints: _Optional[_Iterable[_Union[VariableData, _Mapping]]] = ...) -> None: ...

class VariableData(_message.Message):
    __slots__ = ("variable", "float_datapoints", "geo_datapoints", "status_datapoints")
    VARIABLE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    GEO_DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    variable: str
    float_datapoints: FloatDatapoints
    geo_datapoints: GeoDatapoints
    status_datapoints: StatusDatapoints
    def __init__(self, variable: _Optional[str] = ..., float_datapoints: _Optional[_Union[FloatDatapoints, _Mapping]] = ..., geo_datapoints: _Optional[_Union[GeoDatapoints, _Mapping]] = ..., status_datapoints: _Optional[_Union[StatusDatapoints, _Mapping]] = ...) -> None: ...

class FloatDatapoints(_message.Message):
    __slots__ = ("datapoints",)
    DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    datapoints: _containers.RepeatedCompositeFieldContainer[FloatDatapoint]
    def __init__(self, datapoints: _Optional[_Iterable[_Union[FloatDatapoint, _Mapping]]] = ...) -> None: ...

class FloatDatapoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    value: float
    def __init__(self, timestamp: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class GeoDatapoints(_message.Message):
    __slots__ = ("datapoints",)
    DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    datapoints: _containers.RepeatedCompositeFieldContainer[GeoDatapoint]
    def __init__(self, datapoints: _Optional[_Iterable[_Union[GeoDatapoint, _Mapping]]] = ...) -> None: ...

class GeoDatapoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    value: GeoCoordinate
    def __init__(self, timestamp: _Optional[int] = ..., value: _Optional[_Union[GeoCoordinate, _Mapping]] = ...) -> None: ...

class GeoCoordinate(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class StatusDatapoints(_message.Message):
    __slots__ = ("datapoints",)
    DATAPOINTS_FIELD_NUMBER: _ClassVar[int]
    datapoints: _containers.RepeatedCompositeFieldContainer[StatusDatapoint]
    def __init__(self, datapoints: _Optional[_Iterable[_Union[StatusDatapoint, _Mapping]]] = ...) -> None: ...

class StatusDatapoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    value: str
    def __init__(self, timestamp: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...

class GenericResponse(_message.Message):
    __slots__ = ("success", "error_message", "reason_code")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    reason_code: str
    def __init__(self, success: _Optional[bool] = ..., error_message: _Optional[str] = ..., reason_code: _Optional[str] = ...) -> None: ...

"""IngestService — wraps DataManagementService.SubmitData."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from anedya.sdk.models.common import VariableReading

if TYPE_CHECKING:
    from anedya.sdk._transport.grpc import GrpcTransport
    from anedya.sdk._transport.http import HttpTransport

# Must match the proto package + service name in data_management.proto
_SERVICE = "anedya.v1.datamanagement.DataManagementService"
_METHOD = "SubmitData"


class DatamanagementService:
    """Wraps the DataManagementService.SubmitData endpoint."""

    def __init__(self, transport: GrpcTransport | HttpTransport) -> None:
        self._transport = transport

    def submit_data(
        self,
        data: list[VariableReading] | VariableReading | Any,
        node_id: str = "",
        timeout: float | None = None,
    ) -> Any:
        """Submit variable readings to the API.

        Parameters
        ----------
        data : list[VariableReading] | VariableReading | Any
            The data points to submit (or protobuf request/NodeData).
        node_id : str, optional
            Default node ID for readings that do not specify one.
        timeout : float, optional
            Override the default timeout.

        Returns
        -------
        GenericResponse
            Protobuf response containing success, error_message, and reason_code.
        """
        from anedya.sdk._generated.anedya.v1 import data_management_pb2  # type: ignore[import-untyped]

        if data is None:
            raise ValueError("No data provided to submit_data.")

        if isinstance(data, data_management_pb2.SubmitDataRequest):
            request = data
        elif isinstance(data, data_management_pb2.NodeData):
            request = data_management_pb2.SubmitDataRequest(data=[data])
        elif (
            isinstance(data, (list, tuple))
            and data
            and isinstance(data[0], data_management_pb2.NodeData)
        ):
            request = data_management_pb2.SubmitDataRequest(data=list(data))
        else:
            if not isinstance(data, (list, tuple)):
                raw_readings = [data]
            else:
                raw_readings = list(data)

            # Group readings by node_id -> (variable, type) -> list of datapoint objects
            nodes: dict[str, dict[tuple[str, str], list[Any]]] = {}

            for r in raw_readings:
                r_node_id = getattr(r, "node_id", None) or node_id or ""
                if r_node_id not in nodes:
                    nodes[r_node_id] = {}

                if getattr(r, "float_value", None) is not None:
                    key = (r.variable, "float")
                    if key not in nodes[r_node_id]:
                        nodes[r_node_id][key] = []
                    nodes[r_node_id][key].append(
                        data_management_pb2.FloatDatapoint(
                            timestamp=r.timestamp,
                            value=float(r.float_value),
                        )
                    )
                elif getattr(r, "string_value", None) is not None:
                    key = (r.variable, "status")
                    if key not in nodes[r_node_id]:
                        nodes[r_node_id][key] = []
                    nodes[r_node_id][key].append(
                        data_management_pb2.StatusDatapoint(
                            timestamp=r.timestamp,
                            value=str(r.string_value),
                        )
                    )
                elif getattr(r, "geo_data", None) is not None:
                    key = (r.variable, "geo")
                    if key not in nodes[r_node_id]:
                        nodes[r_node_id][key] = []
                    geo = r.geo_data
                    lat = getattr(geo, "latitude", None)
                    if lat is None:
                        lat = getattr(geo, "lat", 0.0)
                    lng = getattr(geo, "longitude", None)
                    if lng is None:
                        lng = getattr(geo, "long", 0.0)
                    nodes[r_node_id][key].append(
                        data_management_pb2.GeoDatapoint(
                            timestamp=r.timestamp,
                            value=data_management_pb2.GeoCoordinate(
                                latitude=float(lat),
                                longitude=float(lng),
                            ),
                        )
                    )
                else:
                    raise ValueError(
                        f"VariableReading for '{getattr(r, 'variable', 'unknown')}' must specify "
                        "float_value, string_value, or geo_data."
                    )

            proto_node_data = []
            for nid, var_map in nodes.items():
                datapoints = []
                for (var_name, dtype), pts in var_map.items():
                    if dtype == "float":
                        datapoints.append(
                            data_management_pb2.VariableData(
                                variable=var_name,
                                float_datapoints=data_management_pb2.FloatDatapoints(datapoints=pts),
                            )
                        )
                    elif dtype == "geo":
                        datapoints.append(
                            data_management_pb2.VariableData(
                                variable=var_name,
                                geo_datapoints=data_management_pb2.GeoDatapoints(datapoints=pts),
                            )
                        )
                    elif dtype == "status":
                        datapoints.append(
                            data_management_pb2.VariableData(
                                variable=var_name,
                                status_datapoints=data_management_pb2.StatusDatapoints(datapoints=pts),
                            )
                        )
                proto_node_data.append(
                    data_management_pb2.NodeData(node_id=nid, datapoints=datapoints)
                )

            request = data_management_pb2.SubmitDataRequest(data=proto_node_data)

        return self._transport.unary(
            service=_SERVICE,
            method=_METHOD,
            request=request,
            response_type=data_management_pb2.GenericResponse,
            timeout=timeout,
        )

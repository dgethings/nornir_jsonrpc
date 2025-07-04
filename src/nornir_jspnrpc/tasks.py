from nornir.core.task import Result, Task
from nornir_jspnrpc.connection import CONNECTION_NAME
from nornir_jspnrpc.types import (
    RPCBaseModel,
    Response,
    CLIRPC,
    CLIParams,
    GetCommand,
    GetParams,
    GetRPC,
    SetCommand,
    SetParams,
    SetRPC,
    Action,
)
from typing import Iterable, Union, Any
from pydantic import BaseModel

req_id: int = 0
Value = dict[str, Any]


def jsonify(v: BaseModel) -> Value:
    """Create Python struct that can be JSON serialized."""
    return v.model_dump(exclude_none=True, exclude_unset=True, by_alias=True)


def _send_rpc(request: RPCBaseModel, task: Task) -> Result:
    global req_id
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    response = device.post(
        content=request.model_dump_json(exclude_none=True),
    )
    response.raise_for_status()
    reply = Response(**response.json())
    if reply.error:
        return Result(host=task.host, result=reply.error)

    req_id += 1
    assert reply.result
    return Result(host=task.host, result=reply.result)


def jsonrpc_cli(task: Task, cmds: list[str]) -> Result:
    global req_id
    return _send_rpc(
        request=CLIRPC(id=req_id, params=CLIParams(commands=cmds)), task=task
    )


def jsonrpc_get(task: Task, paths: Iterable[Union[str, GetCommand]]) -> Result:
    global req_id
    cmds = [GetCommand(path=p) for p in paths if isinstance(p, str)]
    return _send_rpc(
        request=GetRPC(id=req_id, params=GetParams(commands=cmds)), task=task
    )


def jsonrpc_set(task: Task, cmds: Iterable[SetCommand]) -> Result:
    global req_id
    return _send_rpc(
        request=SetRPC(id=req_id, params=SetParams(commands=cmds)), task=task
    )


def jsonrpc_update_config(
    task: Task, path: str, value: BaseModel | None = None
) -> Result:
    global req_id
    cmd = SetCommand(
        action=Action.UPDATE,
        path=path,
    )
    if value:
        cmd.value = jsonify(v=value)
    return _send_rpc(
        request=SetRPC(id=req_id, params=SetParams(commands=[cmd])), task=task
    )


def jsonrpc_replace_config(
    task: Task, path: str, value: BaseModel | None = None
) -> Result:
    global req_id
    cmd = SetCommand(
        action=Action.REPLACE,
        path=path,
    )
    if value:
        cmd.value = jsonify(v=value)
    return _send_rpc(
        request=SetRPC(id=req_id, params=SetParams(commands=[cmd])), task=task
    )


def jsonrpc_delete_config(
    task: Task, path: str, value: BaseModel | None = None
) -> Result:
    global req_id
    cmd = SetCommand(
        action=Action.DELETE,
        path=path,
    )
    if value:
        cmd.value = jsonify(v=value)
    return _send_rpc(
        request=SetRPC(id=req_id, params=SetParams(commands=[cmd])), task=task
    )

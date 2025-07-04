from nornir_jspnrpc import JSONRPC
from nornir_jspnrpc.types import Action, SetCommand
import pytest
import httpx
from http import HTTPStatus


@pytest.fixture
def client():
    return JSONRPC(
        extras={
            "connection": httpx.Client(
                transport=httpx.MockTransport(
                    lambda _: httpx.Response(
                        HTTPStatus.OK,
                        json={
                            "id": 0,
                            "jsonrpc": "2.0",
                            "result": [{"basic system info": {"version": "v23.10.1"}}],
                        },
                    )
                )
            )
        },
    )


def test_cli(client):
    assert client.cli(["show version"])


def test_get(client):
    assert client.get(["/system/information/version"])


def test_set(client):
    assert client.set(
        [
            SetCommand(
                action=Action.UPDATE,
                path="/interface[name=mgmt0]",
                value={"description": "set-via-json-rpc"},
            )
        ]
    )


def test_update_config(client):
    assert client.update_config(
        path="/interface[name=mgmt0]/description:set-via-json-rpc"
    )


def test_replace_config(client):
    assert client.replace_config(
        path="/interface[name=mgmt0]/description:replaced-via-json-rpc"
    )


def test_delete_config(client):
    assert client.delete_config(path="/interface[name=mgmt0]/description")

# Nornir JSON RPC Plugin
[![GitHub Actions](https://github.com/dgethings/nornir_jsonrpc/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/dgethings/nornir_jsonrpc/actions/)
[![PyPI version](https://badge.fury.io/py/nornir-jsonrpc.svg)](https://badge.fury.io/py/nornir-jsonrpc)
[![Python versions](https://img.shields.io/pypi/pyversions/nornir-jsonrpc.svg)](https://pypi.python.org/pypi/nornir-jsonrpc)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdgethings%2Fnornir_jsonrpc%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
[![PyPI Downloads](https://img.shields.io/pypi/dm/nornir-jsonrpc)](https://pypi.org/project/nornir-jsonrpc/)

Nornir plugin for JSON-RPC.

## Installation

```bash
pip install nornir-jsonrpc
```

```bash
uv add nornir-jsonrpc
```

## Plugins

### Connection

* `jsonrpc`: uses `httpx` to connect to a device and transport JSON-RPC.

### Tasks

* `jsonrpc_cli`: Execute a CLI command.
* `jsonrpc_get`: Retrieve data from the device.
* `jsonrpc_set`: Set data on the device.
* `jsonrpc_update_config`: Update a configuration element.
* `jsonrpc_replace_config`: Replace a configuration element.
* `jsonrpc_delete_config`: Delete a configuration element.

## Usage

```python
from nornir import InitNornir
from nornir_jsonrpc.tasks import jsonrpc_cli
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

result = nr.run(
    task=jsonrpc_cli,
    cmds=["show version"],
)

print_result(result)
```

## License

[MIT](LICENSE)

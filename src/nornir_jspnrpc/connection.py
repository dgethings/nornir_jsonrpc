from typing import Any

import httpx
from pydantic import BaseModel

from nornir.core.configuration import Config


CONNECTION_NAME = "JSONRPC"


class JSONRPC(BaseModel):
    def open(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 433,
        platform: str | None = None,
        extras: dict[str, Any] | None = None,
        configuration: Config | None = None,
    ) -> None:
        if (
            extras
            and "connection" in extras
            and isinstance(extras["connection"], httpx.Client)
        ):
            self.connection = extras["connection"]
        else:
            self.connection = httpx.Client(
                base_url=f"https://{hostname}:{port}/jsonrpc",
                auth=(username, password),
                verify=False,
            )

    def close(self) -> None:
        self.connection.close()

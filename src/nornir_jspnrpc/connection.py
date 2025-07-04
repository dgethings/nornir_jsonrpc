from typing import Any

import httpx

from nornir.core.configuration import Config


CONNECTION_NAME = "JSONRPC"


class JSONRPC:
    def open(
        self,
        hostname: str | None,
        username: str | None = "admin",
        password: str | None = "NokiaSrl1!",
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

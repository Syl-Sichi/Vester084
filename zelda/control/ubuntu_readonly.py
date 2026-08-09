import os
import platform
import socket
from dataclasses import dataclass


@dataclass(frozen=True)
class UbuntuReadonlyCapabilities:
    """Safe, read only host inspection capabilities."""

    @staticmethod
    def system_info(args: list[str]) -> dict[str, str]:
        return {
            "platform": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "hostname": socket.gethostname(),
        }

    @staticmethod
    def environment(args: list[str]) -> dict[str, str]:
        # Return only explicitly requested keys, never the complete environment.
        return {key: os.environ[key] for key in args if key in os.environ}

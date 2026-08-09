from __future__ import annotations

import socket


class UbuntuNetworkCapabilities:
    """Read only network inspection for the local Ubuntu host."""

    @staticmethod
    def network_info(args: list[str]) -> dict[str, object]:
        hostname = socket.gethostname()
        addresses = sorted(
            {
                info[4][0]
                for info in socket.getaddrinfo(hostname, None)
                if info[4] and info[4][0]
            }
        )
        return {"hostname": hostname, "addresses": addresses}

    @staticmethod
    def port_check(args: list[str]) -> dict[str, object]:
        if not args or not args[0].isdigit():
            raise ValueError("port_required")
        port = int(args[0])
        if not 1 <= port <= 65535:
            raise ValueError("invalid_port")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        try:
            result = sock.connect_ex(("127.0.0.1", port))
            return {"host": "127.0.0.1", "port": port, "open": result == 0}
        finally:
            sock.close()

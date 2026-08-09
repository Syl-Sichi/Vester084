from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .core import ControlCore
from .tools import build_registry


class AuditLog:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def write(self, event: dict[str, Any]) -> None:
        self.events.append(event)
        if len(self.events) > 1000:
            del self.events[:-1000]


class RequestHandler(BaseHTTPRequestHandler):
    core: ControlCore
    audit: AuditLog

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send(200, {"ok": True, "service": "zelda-control"})
            return
        if self.path == "/v1/tools":
            self._send(200, {"ok": True, "tools": self.core.registry.describe()})
            return
        self._send(404, {"ok": False, "error": "Not found"})

    def do_POST(self) -> None:
        if self.path != "/v1/command":
            self._send(404, {"ok": False, "error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            command = payload.get("command")
            approved = bool(payload.get("approved", False))
            if not isinstance(command, str) or not command.strip():
                self._send(400, {"ok": False, "error": "command must be a non-empty string"})
                return
            self._send(200, self.core.handle(command, approved=approved))
        except (ValueError, json.JSONDecodeError):
            self._send(400, {"ok": False, "error": "Invalid JSON request"})

    def log_message(self, format: str, *args: Any) -> None:
        return


def create_server(host: str = "127.0.0.1", port: int = 8787) -> ThreadingHTTPServer:
    audit = AuditLog()
    core = ControlCore(build_registry(), audit.write)
    handler = type("ZeldaRequestHandler", (RequestHandler,), {"core": core, "audit": audit})
    return ThreadingHTTPServer((host, port), handler)


def main() -> None:
    server = create_server()
    print("Z.E.L.D.A. control service listening on http://127.0.0.1:8787")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

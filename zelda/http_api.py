from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

from zelda.api import handle_command
from zelda.health import snapshot


class ZeldaHandler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, snapshot())
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path != "/v1/command":
            self._json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 64 * 1024:
                self._json(413, {"error": "request_too_large"})
                return
            payload = json.loads(self.rfile.read(length) or b"{}")
            command = payload.get("command")
            if not isinstance(command, str) or not command.strip():
                self._json(400, {"error": "command_required"})
                return
            self._json(200, handle_command(command.strip()))
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "invalid_request"})

    def log_message(self, format: str, *args) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8787) -> None:
    ThreadingHTTPServer((host, port), ZeldaHandler).serve_forever()

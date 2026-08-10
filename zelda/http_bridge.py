"""Loopback HTTP bridge for native Z.E.L.D.A. clients."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

from zelda.service import ZeldaService

HOST = "127.0.0.1"
PORT = 8765


class _Handler(BaseHTTPRequestHandler):
    service = ZeldaService()

    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "service": "zelda"})
            return
        self._send(404, {"status": "error", "message": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/message":
            self._send(404, {"status": "error", "message": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            message = str(payload.get("message", "")).strip()
            if not message:
                self._send(400, {"status": "error", "message": "message is required"})
                return

            result = self.service.handle_command(message)
            self._send(200, result)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._send(400, {"status": "error", "message": str(exc)})
        except Exception:
            self._send(500, {"status": "error", "message": "Z.E.L.D.A. service error"})

    def log_message(self, _format: str, *_args: object) -> None:
        return


def serve(host: str = HOST, port: int = PORT) -> None:
    server = ThreadingHTTPServer((host, port), _Handler)
    print(f"Z.E.L.D.A. bridge listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()

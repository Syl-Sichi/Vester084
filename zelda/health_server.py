import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from zelda.health import snapshot


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/health", "/ready"):
            self.send_response(404)
            self.end_headers()
            return

        body = snapshot()
        if self.path == "/ready" and not body["ready"]:
            self.send_response(503)
        else:
            self.send_response(200)
        payload = json.dumps(body).encode("utf-8")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args) -> None:
        return


class HealthServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8766) -> None:
        self.server = ThreadingHTTPServer((host, port), HealthHandler)
        self._thread: Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = Thread(target=self.server.serve_forever, name="zelda-health", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None

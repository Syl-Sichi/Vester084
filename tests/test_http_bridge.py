import json
from http.client import HTTPConnection
import threading

from zelda.http_bridge import _Handler
from http.server import ThreadingHTTPServer


def test_health_endpoint():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=2)
        connection.request("GET", "/health")
        response = connection.getresponse()
        payload = json.loads(response.read())
        assert response.status == 200
        assert payload["status"] == "ok"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

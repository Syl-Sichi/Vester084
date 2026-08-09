import json
from urllib.request import urlopen

from zelda.health import set_ready
from zelda.health_server import HealthServer


def test_health_server_exposes_health_and_ready():
    set_ready(True)
    server = HealthServer("127.0.0.1", 0)
    server.start()
    try:
        port = server.server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/health") as response:
            body = json.loads(response.read())
        assert response.status == 200
        assert body["service"] == "zelda"

        with urlopen(f"http://127.0.0.1:{port}/ready") as response:
            assert response.status == 200
    finally:
        server.stop()

from zelda.control.ubuntu_network import UbuntuNetworkCapabilities


def test_network_info_returns_hostname_and_addresses(monkeypatch):
    monkeypatch.setattr("zelda.control.ubuntu_network.socket.gethostname", lambda: "zelda-host")
    monkeypatch.setattr(
        "zelda.control.ubuntu_network.socket.getaddrinfo",
        lambda hostname, port: [(2, 1, 6, "", ("127.0.0.1", 0)), (2, 1, 6, "", ("192.168.1.10", 0))],
    )

    result = UbuntuNetworkCapabilities.network_info([])
    assert result == {"hostname": "zelda-host", "addresses": ["127.0.0.1", "192.168.1.10"]}


def test_port_check_reports_closed_port(monkeypatch):
    class FakeSocket:
        def settimeout(self, value):
            assert value == 1.0

        def connect_ex(self, address):
            assert address == ("127.0.0.1", 54321)
            return 111

        def close(self):
            pass

    monkeypatch.setattr("zelda.control.ubuntu_network.socket.socket", lambda *args, **kwargs: FakeSocket())
    assert UbuntuNetworkCapabilities.port_check(["54321"]) == {
        "host": "127.0.0.1",
        "port": 54321,
        "open": False,
    }


def test_port_check_rejects_invalid_port():
    try:
        UbuntuNetworkCapabilities.port_check(["70000"])
    except ValueError as exc:
        assert str(exc) == "invalid_port"
    else:
        raise AssertionError("expected invalid_port")

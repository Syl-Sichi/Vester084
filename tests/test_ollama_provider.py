import json
from urllib.error import URLError

import pytest

from zelda.control.ollama_provider import OllamaProvider


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def test_ollama_provider_accepts_valid_structured_intent(monkeypatch):
    def fake_urlopen(request, timeout):
        assert request.full_url.endswith("/api/generate")
        assert timeout == 10
        return FakeResponse({"response": json.dumps({"capability": "system.info", "args": []})})

    monkeypatch.setattr("zelda.control.ollama_provider.request.urlopen", fake_urlopen)
    result = OllamaProvider().interpret("show system info")
    assert result.capability == "system.info"
    assert result.args == []


def test_ollama_provider_rejects_unsupported_capability(monkeypatch):
    monkeypatch.setattr(
        "zelda.control.ollama_provider.request.urlopen",
        lambda request, timeout: FakeResponse({"response": json.dumps({"capability": "shell.exec", "args": ["rm", "-rf"]})}),
    )
    with pytest.raises(ValueError, match="capability_not_supported"):
        OllamaProvider().interpret("do something")


def test_ollama_provider_rejects_malformed_response(monkeypatch):
    monkeypatch.setattr(
        "zelda.control.ollama_provider.request.urlopen",
        lambda request, timeout: FakeResponse({"response": json.dumps({"capability": 42, "args": "bad"})}),
    )
    with pytest.raises(ValueError, match="invalid_provider_response"):
        OllamaProvider().interpret("show system info")


def test_ollama_provider_propagates_transport_failure(monkeypatch):
    def fake_urlopen(request, timeout):
        raise URLError("connection refused")

    monkeypatch.setattr("zelda.control.ollama_provider.request.urlopen", fake_urlopen)
    with pytest.raises(URLError):
        OllamaProvider().interpret("show system info")

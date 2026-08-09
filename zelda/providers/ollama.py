import json
import os
import urllib.error
import urllib.request

from zelda.core.models import Intent
from zelda.core.provider import ModelProvider


class OllamaProvider(ModelProvider):
    """Local Ollama provider using Ollama's HTTP API."""

    def __init__(self, model: str | None = None, base_url: str | None = None) -> None:
        self.model = model or os.getenv("ZELDA_OLLAMA_MODEL", "gemma3:4b")
        self.base_url = (base_url or os.getenv("ZELDA_OLLAMA_URL", "http://127.0.0.1:11434")).rstrip("/")

    def understand(self, text: str) -> Intent:
        prompt = (
            "You are the intent engine for Z.E.L.D.A. Return JSON only. "
            "Allowed intent names: system.status, system.time, conversation.unknown. "
            "Schema: {\"name\": string, \"arguments\": object}. "
            f"User command: {text}"
        )
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }).encode()
        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = json.loads(response.read().decode())
            result = json.loads(body["response"])
            name = result.get("name", "conversation.unknown")
            arguments = result.get("arguments", {})
            if name not in {"system.status", "system.time", "conversation.unknown"}:
                name = "conversation.unknown"
            if not isinstance(arguments, dict):
                arguments = {}
            return Intent(name, arguments)
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError):
            return Intent("conversation.unknown", {"text": text})

from __future__ import annotations

import json
from urllib import request

from zelda.control.providers import ProviderIntent


class OllamaProvider:
    """Local Ollama adapter that only returns structured capability intents."""

    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "gemma3") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def interpret(self, text: str) -> ProviderIntent:
        prompt = (
            "Return JSON only with keys capability and args. "
            "Choose only from: system.info, system.processes.read. "
            "If unsupported, return capability unsupported and args [].\n"
            f"Request: {text}"
        )
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False, "format": "json"}).encode()
        req = request.Request(f"{self.base_url}/api/generate", data=payload, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=10) as response:
            body = json.loads(response.read().decode())
        raw = json.loads(body.get("response", "{}"))
        capability = raw.get("capability")
        args = raw.get("args", [])
        if not isinstance(capability, str) or not isinstance(args, list) or not all(isinstance(item, str) for item in args):
            raise ValueError("invalid_provider_response")
        if capability == "unsupported":
            raise ValueError("intent_not_supported")
        if capability not in {"system.info", "system.processes.read"}:
            raise ValueError("capability_not_supported")
        return ProviderIntent(capability, args)

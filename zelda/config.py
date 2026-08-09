import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ZeldaConfig:
    host: str = "127.0.0.1"
    port: int = 8765
    log_level: str = "INFO"
    ai_provider: str = "rules"
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "gemma3"

    @classmethod
    def from_env(cls) -> "ZeldaConfig":
        host = os.getenv("ZELDA_HOST", cls.host)
        port_text = os.getenv("ZELDA_PORT", str(cls.port))
        log_level = os.getenv("ZELDA_LOG_LEVEL", cls.log_level).upper()
        ai_provider = os.getenv("ZELDA_AI_PROVIDER", cls.ai_provider).lower()
        ollama_url = os.getenv("ZELDA_OLLAMA_URL", cls.ollama_url).rstrip("/")
        ollama_model = os.getenv("ZELDA_OLLAMA_MODEL", cls.ollama_model).strip()
        try:
            port = int(port_text)
        except ValueError as exc:
            raise ValueError("ZELDA_PORT must be an integer") from exc
        if not 1 <= port <= 65535:
            raise ValueError("ZELDA_PORT must be between 1 and 65535")
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("ZELDA_LOG_LEVEL is invalid")
        if ai_provider not in {"rules", "ollama"}:
            raise ValueError("ZELDA_AI_PROVIDER is invalid")
        if not ollama_url:
            raise ValueError("ZELDA_OLLAMA_URL cannot be empty")
        if not ollama_model:
            raise ValueError("ZELDA_OLLAMA_MODEL cannot be empty")
        return cls(host=host, port=port, log_level=log_level, ai_provider=ai_provider,
                   ollama_url=ollama_url, ollama_model=ollama_model)

    @property
    def ollama_enabled(self) -> bool:
        return self.ai_provider == "ollama"

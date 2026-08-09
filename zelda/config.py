import os


def use_ollama() -> bool:
    return os.getenv("ZELDA_AI_PROVIDER", "rules").lower() == "ollama"

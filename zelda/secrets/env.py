import os


class EnvironmentSecretStore:
    """Read integration secrets from environment variables only."""

    def get(self, key: str) -> str | None:
        return os.getenv(key)

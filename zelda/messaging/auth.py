from dataclasses import dataclass


@dataclass(frozen=True)
class MessagingCredentialRef:
    """Reference to a credential without storing its secret value."""

    platform: str
    access_token_env: str


class MessagingAuth:
    """Resolves credentials through an injected secret store."""

    def __init__(self, secret_store) -> None:
        self.secret_store = secret_store

    def token(self, credential: MessagingCredentialRef) -> str | None:
        return self.secret_store.get(credential.access_token_env)

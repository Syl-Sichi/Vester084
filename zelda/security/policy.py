from dataclasses import dataclass


@dataclass(frozen=True)
class ClientPolicy:
    client_id: str
    allowed_scopes: frozenset[str]


class AuthorizationPolicy:
    def __init__(self) -> None:
        self._clients: dict[str, ClientPolicy] = {}

    def register(self, client_id: str, scopes: set[str] | frozenset[str]) -> None:
        self._clients[client_id] = ClientPolicy(client_id, frozenset(scopes))

    def allows(self, client_id: str, scope: str) -> bool:
        policy = self._clients.get(client_id)
        return policy is not None and scope in policy.allowed_scopes

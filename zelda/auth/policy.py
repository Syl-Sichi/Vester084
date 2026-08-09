from dataclasses import dataclass


@dataclass(frozen=True)
class ClientPolicy:
    client_id: str
    scopes: frozenset[str]


DEFAULT_CLIENT_POLICIES = {
    "android": ClientPolicy("android", frozenset({"health.read", "command.execute"})),
    "desktop": ClientPolicy("desktop", frozenset({"health.read", "command.execute"})),
}

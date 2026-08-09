from zelda.auth.policy import DEFAULT_CLIENT_POLICIES
from zelda.auth.sessions import SessionManager


class HTTPAuth:
    def __init__(self, sessions: SessionManager | None = None) -> None:
        self.sessions = sessions or SessionManager()

    def issue(self, client_id: str) -> str | None:
        policy = DEFAULT_CLIENT_POLICIES.get(client_id)
        if policy is None:
            return None
        token, _ = self.sessions.create(client_id, set(policy.scopes))
        return token

    def authorize(self, authorization: str | None, scope: str) -> bool:
        if not authorization or not authorization.startswith("Bearer "):
            return False
        token = authorization[7:].strip()
        if not token:
            return False
        return self.sessions.validate(token, scope) is not None

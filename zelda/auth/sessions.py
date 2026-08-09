import hashlib
import secrets
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    session_id: str
    token_hash: str
    client_id: str
    scopes: frozenset[str]
    expires_at: float


class SessionManager:
    """In memory session manager. Raw bearer tokens are never persisted."""

    def __init__(self, ttl_seconds: int = 3600) -> None:
        self.ttl_seconds = ttl_seconds
        self._sessions: dict[str, Session] = {}

    @staticmethod
    def _hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create(self, client_id: str, scopes: set[str]) -> tuple[str, Session]:
        token = secrets.token_urlsafe(32)
        session = Session(
            session_id=secrets.token_hex(16),
            token_hash=self._hash(token),
            client_id=client_id,
            scopes=frozenset(scopes),
            expires_at=time.time() + self.ttl_seconds,
        )
        self._sessions[session.session_id] = session
        return token, session

    def validate(self, token: str, required_scope: str | None = None) -> Session | None:
        token_hash = self._hash(token)
        now = time.time()
        for session_id, session in list(self._sessions.items()):
            if session.expires_at <= now:
                self._sessions.pop(session_id, None)
                continue
            if secrets.compare_digest(session.token_hash, token_hash):
                if required_scope and required_scope not in session.scopes:
                    return None
                return session
        return None

    def revoke(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

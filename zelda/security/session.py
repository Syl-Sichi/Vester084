from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import secrets


@dataclass(frozen=True)
class Session:
    session_id: str
    token_hash: str
    client_id: str
    expires_at: datetime


class SessionManager:
    """Short lived bearer sessions. Only token hashes are retained in memory."""

    def __init__(self, ttl_seconds: int = 3600) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self._sessions: dict[str, Session] = {}

    @staticmethod
    def _hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create(self, client_id: str) -> tuple[str, Session]:
        token = secrets.token_urlsafe(32)
        session = Session(
            session_id=secrets.token_hex(16),
            token_hash=self._hash(token),
            client_id=client_id,
            expires_at=datetime.now(timezone.utc) + self.ttl,
        )
        self._sessions[session.session_id] = session
        return token, session

    def validate(self, token: str) -> Session | None:
        token_hash = self._hash(token)
        now = datetime.now(timezone.utc)
        for session_id, session in list(self._sessions.items()):
            if session.expires_at <= now:
                self._sessions.pop(session_id, None)
                continue
            if secrets.compare_digest(session.token_hash, token_hash):
                return session
        return None

    def revoke(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

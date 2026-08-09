from dataclasses import dataclass

from zelda.auth.sessions import Session, SessionManager


@dataclass(frozen=True)
class MobileSession:
    client_id: str
    session: Session


class MobileSessionManager:
    """Mobile facing session boundary. Tokens remain owned by SessionManager."""

    def __init__(self, sessions: SessionManager | None = None) -> None:
        self.sessions = sessions or SessionManager()

    def create(self, client_id: str) -> tuple[str, MobileSession] | None:
        if client_id != "android":
            return None
        token, session = self.sessions.create(
            client_id,
            {"health.read", "command.execute"},
        )
        return token, MobileSession(client_id, session)

    def authorize(self, token: str, scope: str) -> MobileSession | None:
        session = self.sessions.validate(token, scope)
        if session is None or session.client_id != "android":
            return None
        return MobileSession("android", session)

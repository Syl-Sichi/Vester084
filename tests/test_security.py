from zelda.security.policy import AuthorizationPolicy
from zelda.security.session import SessionManager


def test_session_token_is_valid_until_revoked():
    manager = SessionManager(ttl_seconds=60)
    token, session = manager.create("android")
    assert manager.validate(token) is not None
    assert manager.revoke(session.session_id) is True
    assert manager.validate(token) is None


def test_authorization_is_scoped():
    policy = AuthorizationPolicy()
    policy.register("android", {"command.read"})
    assert policy.allows("android", "command.read")
    assert not policy.allows("android", "command.execute")

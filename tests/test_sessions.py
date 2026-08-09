from zelda.auth.sessions import SessionManager


def test_session_token_is_valid_until_expiry_or_revoke():
    manager = SessionManager(ttl_seconds=60)
    token, session = manager.create("android", {"health.read"})

    assert manager.validate(token, "health.read") is not None
    assert manager.validate(token, "command.execute") is None
    assert manager.revoke(session.session_id) is True
    assert manager.validate(token) is None

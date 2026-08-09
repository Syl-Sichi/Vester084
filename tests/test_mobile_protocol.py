from zelda.mobile.protocol import Envelope, MessageType
from zelda.mobile.session import MobileSessionManager


def test_envelope_round_trip():
    original = Envelope(MessageType.COMMAND, "req-1", {"command": "what time is it"})
    restored = Envelope.from_dict(original.to_dict())
    assert restored == original


def test_android_session_is_scoped():
    manager = MobileSessionManager()
    created = manager.create("android")
    assert created is not None
    token, mobile_session = created
    assert manager.authorize(token, "command.execute") is not None
    assert manager.authorize(token, "admin.execute") is None
    assert mobile_session.client_id == "android"

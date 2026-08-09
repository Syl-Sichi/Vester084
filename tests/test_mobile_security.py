import pytest

from zelda.mobile.security import ConnectionPolicy


def test_connection_policy_limits_frame_size():
    policy = ConnectionPolicy(max_frame_bytes=4)
    with pytest.raises(ValueError, match="frame_too_large"):
        policy.validate_frame_size("hello")


def test_connection_policy_limits_connections():
    policy = ConnectionPolicy(max_connections=2)
    policy.validate_connection_count(1)
    with pytest.raises(RuntimeError, match="connection_limit_reached"):
        policy.validate_connection_count(2)

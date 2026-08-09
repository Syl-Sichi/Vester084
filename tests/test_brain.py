from zelda.app import brain


def test_system_status_is_allowed():
    result = brain.handle("check my computer")
    assert result.success is True
    assert "platform" in result.data


def test_unknown_command_is_safe():
    result = brain.handle("do something unrestricted")
    assert result.success is False


def test_time_is_allowed():
    result = brain.handle("what time is it")
    assert result.success is True
    assert "utc" in result.data

from zelda.control.ubuntu_readonly import UbuntuReadonlyCapabilities


def test_system_info_is_read_only_and_structured():
    result = UbuntuReadonlyCapabilities.system_info([])
    assert "platform" in result
    assert "release" in result
    assert "machine" in result
    assert "hostname" in result


def test_environment_returns_only_requested_keys(monkeypatch):
    monkeypatch.setenv("ZELDA_TEST_VALUE", "safe")
    monkeypatch.setenv("ZELDA_OTHER_VALUE", "hidden")
    assert UbuntuReadonlyCapabilities.environment(["ZELDA_TEST_VALUE"]) == {"ZELDA_TEST_VALUE": "safe"}

from zelda.tools.macos import MacOSApplicationsTool, MacOSSystemStatusTool


def test_macos_system_tool(monkeypatch):
    monkeypatch.setattr(
        "zelda.tools.macos.MacOSSystemCapabilities.system_info",
        lambda _: {"platform": "Darwin", "machine": "x86_64"},
    )
    result = MacOSSystemStatusTool().execute({})
    assert result.success is True
    assert result.data["platform"] == "Darwin"


def test_macos_applications_tool(monkeypatch):
    monkeypatch.setattr(
        "zelda.tools.macos.MacOSSystemCapabilities.app_list",
        lambda _: ["Finder", "Safari"],
    )
    result = MacOSApplicationsTool().execute({})
    assert result.success is True
    assert result.data["applications"] == ["Finder", "Safari"]

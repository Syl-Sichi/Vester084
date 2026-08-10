from pathlib import Path

from zelda.macos_service import LABEL, build_launch_agent


def test_build_launch_agent_contains_local_service_command():
    agent = build_launch_agent("/usr/bin/python3", "/tmp/zelda")
    assert agent["Label"] == LABEL
    assert agent["ProgramArguments"] == ["/usr/bin/python3", "-m", "zelda.http_bridge"]
    assert agent["WorkingDirectory"] == "/tmp/zelda"
    assert agent["RunAtLoad"] is True
    assert agent["KeepAlive"] is True
    assert str(Path.home() / ".zelda" / "logs") in agent["StandardOutPath"]

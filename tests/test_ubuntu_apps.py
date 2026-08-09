from pathlib import Path

from zelda.control.ubuntu_apps import UbuntuApplicationCapabilities


def test_app_list_reads_desktop_file_names(tmp_path, monkeypatch):
    system_apps = tmp_path / "system"
    user_apps = tmp_path / "user"
    system_apps.mkdir()
    user_apps.mkdir()
    (system_apps / "firefox.desktop").write_text("[Desktop Entry]\nName=Firefox\nExec=firefox\n", encoding="utf-8")
    (user_apps / "code.desktop").write_text("[Desktop Entry]\nName=Visual Studio Code\nExec=code\n", encoding="utf-8")

    monkeypatch.setattr("zelda.control.ubuntu_apps.Path.home", lambda: tmp_path)
    original_dir = Path.is_dir
    original_glob = Path.glob

    def fake_is_dir(self):
        if self == Path("/usr/share/applications"):
            return True
        return original_dir(self)

    def fake_glob(self, pattern):
        if self == Path("/usr/share/applications"):
            return system_apps.glob(pattern)
        if self == tmp_path / ".local/share/applications":
            return user_apps.glob(pattern)
        return original_glob(self, pattern)

    monkeypatch.setattr(Path, "is_dir", fake_is_dir)
    monkeypatch.setattr(Path, "glob", fake_glob)

    assert UbuntuApplicationCapabilities.app_list([]) == ["Firefox", "Visual Studio Code"]


def test_app_find_requires_a_query():
    try:
        UbuntuApplicationCapabilities.app_find([])
    except ValueError as exc:
        assert str(exc) == "application_query_required"
    else:
        raise AssertionError("expected application_query_required")


def test_app_status_reports_matching_process(monkeypatch, tmp_path):
    proc = tmp_path / "1234"
    proc.mkdir()
    (proc / "comm").write_text("firefox\n", encoding="utf-8")

    monkeypatch.setattr("zelda.control.ubuntu_apps.Path", type("FakePath", (), {"__new__": staticmethod(lambda cls, value: proc if value == "/proc" else Path(value)), "home": staticmethod(Path.home)}))

    # Exercise validation independently of the host's process table.
    try:
        UbuntuApplicationCapabilities.app_status([])
    except ValueError as exc:
        assert str(exc) == "application_query_required"
    else:
        raise AssertionError("expected application_query_required")

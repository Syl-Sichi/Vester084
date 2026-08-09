from pathlib import Path

from zelda.control.ubuntu_resources import UbuntuResourceCapabilities


def test_memory_read_returns_linux_memory_fields(tmp_path, monkeypatch):
    meminfo = tmp_path / "meminfo"
    meminfo.write_text(
        "MemTotal:       1024 kB\n"
        "MemAvailable:    512 kB\n"
        "SwapTotal:      256 kB\n"
        "SwapFree:       128 kB\n",
        encoding="utf-8",
    )

    original_exists = Path.exists
    original_read_text = Path.read_text

    def fake_exists(self):
        return True if self == Path("/proc/meminfo") else original_exists(self)

    def fake_read_text(self, encoding=None):
        if self == Path("/proc/meminfo"):
            return meminfo.read_text(encoding="utf-8")
        return original_read_text(self, encoding=encoding)

    monkeypatch.setattr(Path, "exists", fake_exists)
    monkeypatch.setattr(Path, "read_text", fake_read_text)

    result = UbuntuResourceCapabilities.memory_read([])
    assert result == {
        "MemTotal": 1024 * 1024,
        "MemAvailable": 512 * 1024,
        "SwapTotal": 256 * 1024,
        "SwapFree": 128 * 1024,
    }


def test_disk_read_uses_requested_path(monkeypatch):
    class Usage:
        total = 100
        used = 40
        free = 60

    captured = {}

    def fake_disk_usage(path):
        captured["path"] = path
        return Usage()

    monkeypatch.setattr("zelda.control.ubuntu_resources.shutil.disk_usage", fake_disk_usage)
    result = UbuntuResourceCapabilities.disk_read(["/tmp"])
    assert captured["path"] == Path("/tmp")
    assert result == {"total": 100, "used": 40, "free": 60}

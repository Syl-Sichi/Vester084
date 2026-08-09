from pathlib import Path

from zelda import setup


def test_first_run_setup(monkeypatch, tmp_path):
    monkeypatch.setattr(setup, "CONFIG_DIR", tmp_path / ".zelda")
    monkeypatch.setattr(setup, "CONFIG_FILE", tmp_path / ".zelda" / "setup.json")

    config = setup.run_setup()

    assert config["initialized"] is True
    assert setup.is_initialized() is True
    assert Path(config["workspace"]).exists()

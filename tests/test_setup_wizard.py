from pathlib import Path

import zelda.setup_wizard as wizard


def test_first_run_setup_creates_config(monkeypatch, tmp_path):
    config_dir = tmp_path / ".zelda"
    monkeypatch.setattr(wizard, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(wizard, "CONFIG_FILE", config_dir / "config.json")

    result = wizard.run_setup()

    assert result["setup_complete"] == "true"
    assert (config_dir / "config.json").exists()
    assert (config_dir / "workspace").exists()

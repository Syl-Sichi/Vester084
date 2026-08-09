from zelda.macos import cli


def test_macos_cli_reports_system_and_apps(monkeypatch, capsys):
    monkeypatch.setattr(cli.MacOSSystemCapabilities, "system_info", lambda _: {"platform": "Darwin"})
    monkeypatch.setattr(cli.MacOSSystemCapabilities, "app_list", lambda _: ["Finder", "Safari"])

    cli.main()
    output = capsys.readouterr().out

    assert "Z.E.L.D.A. macOS runtime" in output
    assert '"platform": "Darwin"' in output
    assert "Finder" in output
    assert "Safari" in output

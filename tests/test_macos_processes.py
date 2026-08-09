from zelda.macos.processes import MacOSProcessCapabilities


def test_process_parser(monkeypatch):
    class Result:
        returncode = 0
        stdout = " 123 /Applications/Test.app/Contents/MacOS/Test\n456 /usr/bin/python3\n"

    monkeypatch.setattr("zelda.macos.processes.subprocess.run", lambda *args, **kwargs: Result())
    assert MacOSProcessCapabilities.processes_read([]) == [
        {"pid": 123, "name": "/Applications/Test.app/Contents/MacOS/Test"},
        {"pid": 456, "name": "/usr/bin/python3"},
    ]

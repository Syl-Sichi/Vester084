from zelda.control.ubuntu_processes import UbuntuProcessCapabilities


def test_processes_read_returns_structured_records():
    processes = UbuntuProcessCapabilities.processes_read([])
    assert isinstance(processes, list)
    if processes:
        assert "pid" in processes[0]
        assert "name" in processes[0]
        assert isinstance(processes[0]["pid"], int)

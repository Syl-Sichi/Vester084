from zelda.desktop import DesktopShell


def test_desktop_shell_defaults_to_chat():
    shell = DesktopShell()
    state = shell.snapshot()
    assert state["assistant_name"] == "Z.E.L.D.A."
    assert state["status"] == "Ready"
    assert state["active_view"] == "Chat"


def test_desktop_shell_can_switch_views_and_store_messages():
    shell = DesktopShell()
    shell.select_view("Security")
    shell.add_message("Ready for approval")
    shell.set_status("Awaiting confirmation")

    state = shell.snapshot()
    assert state["active_view"] == "Security"
    assert state["messages"] == ["Ready for approval"]
    assert state["status"] == "Awaiting confirmation"

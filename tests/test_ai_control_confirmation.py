import pytest

from zelda.control.ai_control import AIControlService
from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.control.write_control import WriteController


def make_service():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    policy = CapabilityPolicy.from_registry(registry)
    controller = WriteController(lambda capability, args: {"written": True, "args": args})
    return AIControlService(registry, policy, write_controller=controller)


def test_write_request_returns_confirmation_details():
    service = make_service()
    result = service.request_write("workspace.note.write", ["note.txt", "hello"])
    assert result["accepted"] is False
    assert result["confirmation_required"] is True
    assert result["confirmation_token"]
    assert result["capability"] == "workspace.note.write"


def test_write_confirmation_executes_once():
    service = make_service()
    pending = service.request_write("workspace.note.write", ["note.txt", "hello"])
    result = service.confirm_write(pending["confirmation_token"])
    assert result["accepted"] is True
    with pytest.raises(ValueError, match="confirmation_not_found"):
        service.confirm_write(pending["confirmation_token"])


def test_cancelled_write_cannot_execute():
    service = make_service()
    pending = service.request_write("workspace.note.write", ["note.txt", "hello"])
    service.cancel_write(pending["confirmation_token"])
    with pytest.raises(ValueError, match="confirmation_not_found"):
        service.confirm_write(pending["confirmation_token"])

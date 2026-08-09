from zelda.ai.control import AIControlService


def test_control_service_normalizes_and_parses_command():
    result = AIControlService().process("   open   messages   ")
    assert result.accepted is True
    assert result.action == "open"
    assert result.metadata["arguments"]["text"] == "messages"


def test_control_service_uses_injected_executor():
    calls = []

    def executor(action, arguments):
        calls.append((action, arguments))
        return {"ok": True}

    result = AIControlService(executor).process("send hello")
    assert calls == [("send", {"text": "hello"})]
    assert result.metadata["result"] == {"ok": True}

import unittest

from zelda.control.ai_control import AIControlService
from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.control.providers import ProviderIntent, RulesProvider


class ControlCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = CapabilityRegistry()
        register_ubuntu_readonly_capabilities(self.registry)
        self.policy = CapabilityPolicy.from_registry(self.registry)
        self.core = AIControlService(self.registry, self.policy, provider=RulesProvider())

    def test_system_info_command(self) -> None:
        result = self.core.handle("system info")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["capability"], "system.info")

    def test_memory_command(self) -> None:
        result = self.core.handle("show memory")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["capability"], "system.memory.read")

    def test_unknown_command_is_not_executed(self) -> None:
        with self.assertRaises(ValueError):
            self.core.handle("run a shell command")

    def test_unsupported_capability_is_not_executed(self) -> None:
        class UnsupportedProvider:
            def interpret(self, text):
                return ProviderIntent("shell.exec", ["id"])

        service = AIControlService(self.registry, self.policy, provider=UnsupportedProvider())
        with self.assertRaises(PermissionError):
            service.handle("run a shell command")


if __name__ == "__main__":
    unittest.main()

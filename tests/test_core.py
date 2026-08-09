import unittest

from zelda.core import ControlCore
from zelda.tools import build_registry


class ControlCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit_events = []
        self.core = ControlCore(build_registry(), self.audit_events.append)

    def test_status_command(self) -> None:
        result = self.core.handle("system status")
        self.assertTrue(result["ok"])
        self.assertEqual(result["tool"], "system.status")

    def test_time_command(self) -> None:
        result = self.core.handle("what time is it")
        self.assertTrue(result["ok"])
        self.assertIn("utc", result["result"])

    def test_unknown_command_is_not_executed(self) -> None:
        result = self.core.handle("run a shell command")
        self.assertFalse(result["ok"])
        self.assertIsNone(result.get("tool"))

    def test_audit_event_is_created(self) -> None:
        self.core.handle("system status")
        self.assertEqual(len(self.audit_events), 1)


if __name__ == "__main__":
    unittest.main()

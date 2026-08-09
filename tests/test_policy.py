import pytest

from zelda.control.capabilities import Capability, CapabilityRegistry
from zelda.control.policy import CapabilityPolicy


def test_policy_is_derived_from_registered_capabilities():
    registry = CapabilityRegistry()
    registry.register(Capability("file.read", "Read a file", lambda args: None))
    policy = CapabilityPolicy.from_registry(registry)
    assert policy.permits("file.read")
    assert policy.snapshot() == ("file.read",)


def test_policy_rejects_unlisted_capability():
    policy = CapabilityPolicy(frozenset({"file.read"}))
    with pytest.raises(PermissionError, match="capability_not_allowed"):
        policy.require("file.write")

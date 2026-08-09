import pytest

from zelda.control.providers import ProviderIntent, RulesProvider, build_provider


def test_rules_provider_returns_structured_intent():
    result = RulesProvider().interpret("  SHOW   SYSTEM   INFO ")
    assert isinstance(result, ProviderIntent)
    assert result.capability == "system.info"
    assert result.args == []


def test_rules_provider_rejects_unknown_request():
    with pytest.raises(ValueError, match="intent_not_supported"):
        RulesProvider().interpret("delete everything")


def test_provider_factory_has_safe_default():
    assert isinstance(build_provider("rules"), RulesProvider)


def test_unimplemented_provider_is_explicitly_rejected():
    with pytest.raises(ValueError, match="ai_provider_not_implemented:ollama"):
        build_provider("ollama")

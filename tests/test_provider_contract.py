import pytest

from zelda.control.ollama_provider import OllamaProvider
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


def test_provider_factory_builds_configured_ollama_provider():
    provider = build_provider(
        "ollama",
        ollama_url="http://localhost:11434/",
        ollama_model="test-model",
    )
    assert isinstance(provider, OllamaProvider)
    assert provider.base_url == "http://localhost:11434"
    assert provider.model == "test-model"


def test_provider_factory_rejects_unknown_provider():
    with pytest.raises(ValueError, match="ai_provider_not_implemented:unknown"):
        build_provider("unknown")

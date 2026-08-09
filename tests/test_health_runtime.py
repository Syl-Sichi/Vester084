from zelda.health import snapshot
from zelda.health_runtime import HealthRuntime


def test_health_runtime_toggles_readiness():
    runtime = HealthRuntime("127.0.0.1", 0)
    runtime.start()
    try:
        assert snapshot()["ready"] is True
    finally:
        runtime.stop()
    assert snapshot()["ready"] is False

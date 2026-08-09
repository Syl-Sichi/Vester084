import pytest

from zelda.mobile.rate_limit import RateLimiter


def test_rate_limiter_allows_within_window():
    limiter = RateLimiter(max_events=2, window_seconds=10)
    assert limiter.allow("client", now=100)
    assert limiter.allow("client", now=101)
    assert not limiter.allow("client", now=102)
    assert limiter.allow("client", now=111)


def test_rate_limiter_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        RateLimiter(max_events=0)

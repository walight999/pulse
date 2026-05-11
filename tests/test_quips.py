"""Test quips — stability + threshold logic."""
import quips


def test_stable_within_same_call():
    """Calling for_empty() twice in a row → same result (same day)."""
    a = quips.for_empty()
    b = quips.for_empty()
    assert a == b, "Quips should be stable within a session"


def test_spike_threshold():
    """for_spike() should return None for normal usage, str for spike."""
    # Today equals average → no spike
    assert quips.for_spike(today_usd=50, avg_usd=50) is None
    # Today is 4x average → spike
    result = quips.for_spike(today_usd=200, avg_usd=50)
    assert isinstance(result, str) and len(result) > 0


def test_roi_threshold():
    """for_roi() returns None for low ROI, returns str for high."""
    assert quips.for_roi(0.5) is None
    assert quips.for_roi(1.0) is None
    high = quips.for_roi(15.0)
    assert isinstance(high, str)
    # 15× should be inserted into the quip via {n}
    assert "15" in high or "16" in high or "×" in high


def test_streak_threshold():
    """for_streak() returns None below threshold, returns str at/above."""
    assert quips.for_streak(0) is None
    assert quips.for_streak(5) is None  # below 7-day threshold
    week = quips.for_streak(7)
    assert isinstance(week, str)
    long_run = quips.for_streak(30)
    assert isinstance(long_run, str)

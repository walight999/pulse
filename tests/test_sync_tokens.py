"""Test Claude Code token parser — pricing accuracy."""
import sync_tokens


def test_pricing_dict_has_current_models():
    """Verify pricing table has the models we expect to see."""
    keys = sync_tokens.PRICING.keys()
    assert any("opus" in k.lower() for k in keys), "Opus model missing from pricing"
    assert any("sonnet" in k.lower() for k in keys), "Sonnet model missing from pricing"
    assert any("haiku" in k.lower() for k in keys), "Haiku model missing from pricing"


def test_opus_pricing_has_cache_split():
    """Opus must have separate cw_5m + cw_1h rates."""
    opus_keys = [k for k in sync_tokens.PRICING if "opus" in k.lower()]
    assert opus_keys, "Need at least one Opus entry"
    rates = sync_tokens.PRICING[opus_keys[0]]
    assert "cw_5m" in rates, "5min cache rate missing"
    assert "cw_1h" in rates, "1hr cache rate missing"
    assert rates["cw_1h"] > rates["cw_5m"], "1hr cache should cost more than 5min"


def test_cache_ratios_match_anthropic_spec():
    """Per Anthropic: 5min cache = 1.25x input, 1hr cache = 2x input."""
    for model, rates in sync_tokens.PRICING.items():
        if "cw_5m" not in rates or "cw_1h" not in rates:
            continue
        ratio_5m = rates["cw_5m"] / rates["input"]
        ratio_1h = rates["cw_1h"] / rates["input"]
        # Anthropic spec: 5m = 1.25x, 1h = 2x (allow tiny rounding)
        assert 1.20 <= ratio_5m <= 1.30, f"{model}: 5m ratio {ratio_5m:.3f} not ~1.25x"
        assert 1.90 <= ratio_1h <= 2.10, f"{model}: 1h ratio {ratio_1h:.3f} not ~2x"

"""Test tier feature flag system."""
from unittest.mock import patch


def test_default_tier_is_free(tmp_path):
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        assert account.get_tier() == "free"


def test_set_then_get_tier(tmp_path):
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        for tier in ("free", "pro", "team", "enterprise"):
            account.set_tier(tier)
            assert account.get_tier() == tier


def test_invalid_tier_rejected(tmp_path):
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        try:
            account.set_tier("ultra")  # type: ignore[arg-type]
        except ValueError:
            pass
        else:
            assert False, "expected ValueError for unknown tier"


def test_tier_inheritance(tmp_path):
    """Higher tiers inherit flags from cheaper tiers."""
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        account.set_tier("free")
        assert account.feature_enabled("subscription_tracker")
        assert not account.feature_enabled("cloud_sync")
        assert not account.feature_enabled("team_dashboard")
        assert not account.feature_enabled("sso_saml")

        account.set_tier("pro")
        assert account.feature_enabled("subscription_tracker")  # inherited
        assert account.feature_enabled("cloud_sync")  # own
        assert not account.feature_enabled("team_dashboard")
        assert not account.feature_enabled("sso_saml")

        account.set_tier("team")
        assert account.feature_enabled("cloud_sync")  # inherited from pro
        assert account.feature_enabled("team_dashboard")  # own
        assert not account.feature_enabled("sso_saml")

        account.set_tier("enterprise")
        assert account.feature_enabled("cloud_sync")
        assert account.feature_enabled("team_dashboard")
        assert account.feature_enabled("sso_saml")


def test_tier_for_feature(tmp_path):
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        assert account.tier_for_feature("subscription_tracker") == "free"
        assert account.tier_for_feature("cloud_sync") == "pro"
        assert account.tier_for_feature("team_dashboard") == "team"
        assert account.tier_for_feature("sso_saml") == "enterprise"
        assert account.tier_for_feature("nonexistent_flag") is None


def test_corrupt_tier_falls_back_to_free(tmp_path):
    """If someone hand-edits the DB with garbage, get_tier() must not crash."""
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        db.init_db()
        db.set_setting("pulse_tier", "garbage")
        assert account.get_tier() == "free"


def test_tier_display(tmp_path):
    import db, account
    test_db = tmp_path / "tier.db"
    with patch.object(db, "DB_PATH", test_db):
        account.set_tier("pro")
        d = account.tier_display()
        assert d["name"] == "Pro"
        assert "$9" in d["price_label"]
        assert d["next_tier"] == "team"

        # explicit tier override
        ent = account.tier_display("enterprise")
        assert ent["name"] == "Enterprise"
        assert ent["next_tier"] is None

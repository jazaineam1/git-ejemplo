"""Deterministic tests of history, URL SKU isolation and promotional evidence."""
from datetime import datetime, timedelta, timezone
import tempfile
from pathlib import Path
import json
import unittest

from scripts.update_history import canonical_url, key_for, observed_price, merge_history, detect_deals, run


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)

    def test_tracking_parameters_do_not_split_product(self):
        self.assertEqual(canonical_url("https://SHOP.test/pc?sku=16&utm_source=ad"),
                         canonical_url("https://shop.test/pc?sku=16"))

    def test_sku_difference_kept(self):
        a = {"url": "https://shop.test/pc?sku=16", "seller": "test"}
        b = {"url": "https://shop.test/pc?sku=32", "seller": "test"}
        self.assertNotEqual(key_for(a), key_for(b))

    def test_unverified_coupon_not_subtracted(self):
        o = {"currency": "COP", "price": 5000000, "discount": 20, "coupon": 400000}
        self.assertEqual(observed_price(o), 4000000)
        o["coupon_status"] = "checkout_verified"
        self.assertEqual(observed_price(o), 3600000)

    def test_daily_idempotence(self):
        o = {"key": "k1", "observed_at": self.now.isoformat(), "price_cop": 3000000}
        self.assertEqual(len(merge_history([o], [o, o], self.now)), 1)

    def test_discount_needs_three_prior_days(self):
        def row(days, price):
            return {"key": "k", "title": "PC RTX", "seller": "Store", "url": "https://shop.test/p",
                    "source": "api", "observed_at": (self.now - timedelta(days=days)).isoformat(), "price_cop": price}
        two = [row(5, 5000000), row(4, 5000000), row(0, 4000000)]
        self.assertEqual(detect_deals(two, self.now), [])
        three = [row(6, 5000000)] + two
        result = detect_deals(three, self.now)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["saving_cop"], 1000000)
        self.assertEqual(result[0]["drop_pct"], 20)

    def test_complete_roundtrip_without_offers(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            (root / "offers.json").write_text(json.dumps({"offers": []}))
            (root / "price-history.json").write_text(json.dumps({"observations": []}))
            hist, deals = run(root, self.now)
            self.assertEqual(hist, [])
            self.assertEqual(deals, [])
            self.assertEqual(json.loads((root / "deals.json").read_text())["deals"], [])


if __name__ == "__main__":
    unittest.main()

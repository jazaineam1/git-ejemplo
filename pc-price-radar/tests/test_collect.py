"""Offline tests. No network, keys or invented offers."""
import unittest
from scripts.collect_offers import extract_specs, as_offer, collect, safe_url

class CollectorTests(unittest.TestCase):
    def test_specs(self):
        s=extract_specs("Lenovo Legion RTX 4060 8GB GDDR6 RAM 32GB SSD 1TB OLED")
        self.assertEqual((s["ram"],s["ssd"],s["vram"],s["gpu"],s["screen"]),(32,1024,8,"nvidia","OLED"))
    def test_unknown_specs(self):
        self.assertIsNone(extract_specs("Laptop RTX 4060")["ram"])
    def test_refuse_ambiguous_usd_amount(self):
        self.assertIsNone(as_offer({"title":"Laptop","link":"https://example.com/a","extracted_price":799},"2026-10-25"))
    def test_reject_unsafe_url(self):
        self.assertFalse(safe_url("javascript:alert(1)"))
    def test_dedupe(self):
        item={"title":"RTX 4060","link":"https://shop.example/x","extracted_price":4700000}
        self.assertEqual(len(collect([{"shopping_results":[item,item]}],"2026-10-25")),1)
    def test_no_invented_coupon(self):
        obj=as_offer({"title":"RTX 4060","link":"https://shop.example/pc","extracted_price":4700000,"extracted_old_price":5000000},"2026-10-25")
        self.assertEqual(obj["coupon"],0)
        self.assertIsNone(obj["shipping"])
        self.assertFalse(obj["verified"])

if __name__=="__main__":unittest.main()

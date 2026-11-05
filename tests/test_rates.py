import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_explicit_standard_rates(self):
        for zone, expected in [("local", 8.0), ("regional", 11.0)]:
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, service="standard"), expected)

    def test_express_rates(self):
        for zone, expected in [("local", 15.0), ("regional", 18.0)]:
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, service="express"), expected)
                self.assertEqual(shipping_quote(2, zone, "express"), expected)

    def test_fractional_weights_are_rounded(self):
        for zone, base in [("local", 5.0), ("regional", 8.0)]:
            for service, surcharge in [("standard", 0.0), ("express", 7.0)]:
                with self.subTest(zone=zone, service=service):
                    self.assertEqual(
                        shipping_quote(1.234, zone, service),
                        base + surcharge + 1.85,
                    )

    def test_invalid_weight(self):
        for service in ["standard", "express"]:
            for weight in [0, -1]:
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service)

    def test_invalid_zone(self):
        for service in ["standard", "express"]:
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service)

    def test_invalid_service(self):
        for zone in ["local", "regional"]:
            for service in ["overnight", "Express", ""]:
                with self.subTest(zone=zone, service=service):
                    with self.assertRaisesRegex(ValueError, "unknown service"):
                        shipping_quote(2, zone, service)

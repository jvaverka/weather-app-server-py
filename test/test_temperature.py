from app.temperature import Temperature
from flask import Flask
import unittest


class TestTemperature(unittest.TestCase):
    def test_empty_payload(self):
        app = Flask(__name__)
        with app.app_context():
            self.assertIsNone(Temperature("").value)
            self.assertIsNone(Temperature("""""").value)
            self.assertIsNone(Temperature({}).value)

    def test_valid_payload(self):
        app = Flask(__name__)
        with app.app_context():
            p = {
              "unitCode": "wmoUnit:degC",
              "value": 6.3899999999999997,
              "qualityControl": "V"
            }
            t = Temperature(p)
            self.assertEqual(t.unit, "degC")
            self.assertTrue(t.has_value())
            self.assertAlmostEquals(t.value, 6.39)

    def test_invalid_payload(self):
        app = Flask(__name__)
        with app.app_context():
            p = {
              "invalidunitCode": "wmoUnit:degC",
              "invalidvalue": 6.3899999999999997,
              "invalidqualityControl": "V"
            }
            t = Temperature(p)
            self.assertEqual(t.unit, "")
            self.assertFalse(t.has_value())
            self.assertIsNone(t.value)

if __name__ == "__main__":
    unittest.main()


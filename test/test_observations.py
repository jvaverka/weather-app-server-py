from app.observations import Observation, ObservationList
from flask import Flask
import json
import unittest


class TestObservation(unittest.TestCase):
    def test_empty_payload(self):
        app = Flask(__name__)
        with app.app_context():
            obs = Observation({})
            self.assertEqual(obs.station, "")
            self.assertIsNone(obs.timestamp)
            self.assertFalse(obs.temperature.has_value())

    def test_valid_payload(self):
        app = Flask(__name__)
        with open("test/valid_lastest_payload.json", "r") as file:
            data = json.load(file)
            with app.app_context():
                obs = Observation(data)
                print(obs.station)
                self.assertEqual(obs.station, "0536W")
                self.assertEqual(obs.timestamp.date().strftime("%Y-%m-%d"), "2024-02-20")
                self.assertTrue(obs.temperature.has_value())
                self.assertAlmostEqual(obs.temperature.value, 6.39)

class TestObservationList(unittest.TestCase):
    def test_empty_payload(self):
        app = Flask(__name__)
        with app.app_context():
            obs_list = ObservationList({})
            self.assertEqual(obs_list.features, [])

    def test_valid_payload(self):
        app = Flask(__name__)
        with open("test/valid_collection_payload.json", "r") as file:
            data = json.load(file)
            with app.app_context():
                obs = ObservationList(data)
                self.assertEqual(len(obs.features), 390)
                self.assertEqual(obs.features[0].station, "0004W")
                self.assertEqual(obs.features[0].timestamp.date().strftime("%Y-%m-%d"), "2024-02-20")
                self.assertTrue(obs.features[0].temperature.has_value())
                self.assertAlmostEqual(obs.features[0].temperature.value, 7.33)

    def test_valid_payload2(self):
        app = Flask(__name__)
        with open("test/valid_collection_payload2.json", "r") as file:
            data = json.load(file)
            with app.app_context():
                obs = ObservationList(data)
                self.assertEqual(len(obs.features), 424)
                self.assertEqual(obs.features[0].station, "0004W")
                self.assertEqual(obs.features[0].timestamp.date().strftime("%Y-%m-%d"), "2024-02-20")
                self.assertTrue(obs.features[0].temperature.has_value())
                self.assertAlmostEqual(obs.features[0].temperature.value, 17.94)

if __name__ == "__main__":
    unittest.main()

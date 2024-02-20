from .models import single_observation_schema, many_observations_schema 
from .temperature import Temperature
from datetime import datetime
from flask import current_app as app
from jsonschema import validate
from typing import Dict, List, Optional


class ObservationList(List):
    """A generic class representing an list of observation features.

    Converts a valid observation payload into an object which
    contains many measurements taken at a particular weather station
    over various different points in time."""
    def __init__(self, payload: Dict[str, str]):
        self.payload = payload
        self.features: List[Observation] = []
        if self._is_valid_payload():
            features = payload["features"]
            for f in features:
                self.features.append(Observation(f))
        return

    def has_features(self) -> bool:
        "Return true if the list of observation contains even a single feature."
        return True if len(self.features) > 0 else False

    def _is_valid_payload(self) -> bool:
        """Attempts to validate observation payload against expected json-schema.

        If the payload is successfully validated then return true,
        otherwise add a warning message to the application logger and return false."""
        try:
            validate(instance=self.payload, schema=many_observations_schema)
            return True
        except Exception as e:
            app.logger.warning("Invalid observation feature list: {}".format(self.payload))
            return False

class Observation:
    """A generic class representing an observation feature.

    Converts a valid observation payload into an object which
    contains many measurements taken at a particular weather station."""
    def __init__(self, payload: Dict):
        self.payload = payload
        self.station: str
        self.timestamp: Optional[datetime]
        self.temperature: Temperature
        if self._is_valid_payload():
            properties = payload["properties"]
            self.station = properties["station"].split('/')[-1]
            self.timestamp = datetime.fromisoformat(properties["timestamp"])
            self.temperature = Temperature(properties["temperature"])
        else:
            self.station = ""
            self.timestamp = None
            self.temperature = Temperature({})
        return

    def _is_valid_payload(self) -> bool:
        """Attempts to validate observation payload against expected json-schema.

        If the payload is successfully validated then return true,
        otherwise add a warning message to the application logger and return false."""
        try:
            validate(instance=self.payload, schema=single_observation_schema)
            return True
        except Exception as e:
            app.logger.warning("Invalid observation feature: {}".format(self.payload))
            return False

    def has_station(self):
        "Returns true if station is not empty, otherwise returns false."
        return self.station != ""

    def get_station(self):
        "Returns the station id."
        return self.station

    def get_timestamp(self):
        "Returns the timestamp id."
        return self.timestamp

    def get_temperature_celsius(self):
        "Returns the temperature id."
        return self.temperature.celsius()

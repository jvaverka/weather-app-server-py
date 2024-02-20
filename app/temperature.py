from .models import temperature_schema
from flask import current_app as app
from jsonschema import validate
from typing import Dict, Optional


class Temperature:
    """A generic class representing a temperature feature.

    Converts a valid temperature payload into a temperature object."""
    def __init__(self, payload: Dict[str, str]):
        self.payload = payload
        self.unit: str
        self.value: Optional[int]
        if self._is_valid_payload():
            self.unit = payload["unitCode"].split(':')[-1]
            self.value = payload["value"]
        else:
            self.unit = ""
            self.value = None
        return

    def _is_valid_payload(self) -> bool:
        """Attempts to validate temperature payload against expected json-schema.

        If the payload is successfully validated then return true,
        otherwise add a warning message to the application logger and return false."""
        try:
            validate(instance=self.payload, schema=temperature_schema)
            return True
        except Exception as e:
            app.logger.warning("Invalid temperature feature: {}".format(self.payload))
            return False

    def has_value(self) -> bool:
        "Returns true if temperature value exists, otherwise returns false."
        return self.value is not None

    def celsius(self) -> float:
        "Returns the temperature value in degrees celsius."
        if self.unit == "degF":
            return (self.value - 32) * (5/9)
        else:
            return self.value

    def fahrenheit(self) -> float:
        "Returns the temperature value in degrees fahrenheit."
        if self.unit == "degC":
            return (self.value * 9/5) + 32


# Allows us to use `max` function on list of temperatures
def __ge__(t1: Temperature, t2: Temperature):
    return t1.value > t2.value

# Allows us to use `min` function on list of temperatures
def __le__(t1: Temperature, t2: Temperature):
    return t1.value < t2.value

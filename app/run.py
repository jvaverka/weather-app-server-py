from .observations import Observation, ObservationList
from .temperature import Temperature
from flask import Flask, request
from flask_cors import CORS
from typing import DefaultDict, Optional
import collections
import datetime
import logging
import os
import requests


NWS_ROOT = os.environ["NATIONAL_WEATHER_SERVICE_ROOT_URL"]
CLIENT_ROOT = os.environ["CLIENT_ROOT_URL"]

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": CLIENT_ROOT}})

logging.getLogger('flask_cors').level = logging.DEBUG

# Return string to indicate that server is up and running.
@app.route("/")
def index():
    return "Hello World!"

# Endpoint to return latest observation at a given station.
@app.route("/api/last")
def get_current_temperature():
    # Construct request using environment variables and query parameters.
    station_id = request.args.get("stationId")
    unit = request.args.get("unit")
    query = "{}/stations/{}/observations/latest".format(NWS_ROOT, station_id)
    response = requests.get(query)
    # Create an `Observation` based on the response.
    observation = Observation(response.json())
    # If there was a problem with the response
    # or the observation had no temperature value
    # then return an empty string.
    if not observation.temperature.has_value():
        return ""
    else: # Otherwise return a formatted, fahrenheit temperature value.
        temp_f = Temperature.fahrenheit(observation.temperature)
        return "{:0.1f}".format(temp_f)

# Endpoint to return last weeks worth of observations at a given station.
@app.route("/api/week")
def get_weekly_temperatures():
    # Construct request using environment variables and query parameters.
    station_id = request.args.get("stationId")
    query = "{}/stations/{}/observations".format(NWS_ROOT, station_id)
    response = requests.get(query)
    # Create an `ObservationList` based on the response.
    observations = ObservationList(response.json())
    # If no features were created in the list, then return an empty array.
    if not observations.has_features():
        app.logger.warning("Observations has no features available.")
        return []
    # If features exist, then use the timestamp of the latest feature
    # to generate a list of keys corresponding to each day in the last week.
    latest_observation = observations.features[0]
    days_in_week = [latest_observation.timestamp - datetime.timedelta(days=day) for day in range(7)]
    week_keys = ["{}-{}-{}".format(dt.year, dt.month, dt.day) for dt in days_in_week]
    # Create a dictionary with a key for every day in the last week
    # and let each key's value be a list of every observation from that day.
    agg_obs: DefaultDict[str, list] = collections.defaultdict(list)
    for o in observations.features:
        if not o.temperature.has_value():
            continue  # do not include null values
        key = "{}-{}-{}".format(o.timestamp.year, o.timestamp.month, o.timestamp.day)
        if key in week_keys:
            agg_obs[key].append(Temperature.fahrenheit(o.temperature))
    # Create an array of dictionaries for each row in the table.
    extremes = []
    for key, value in agg_obs.items():
        extremes.append({
            "timestamp": key,
            "temperature": {
                "low": "{:0.1f}".format(min(value)),
                "high": "{:0.1f}".format(max(value))}
        })
    return extremes

import itertools
import os

import joblib
import numpy as np
import pandas as pd
import requests

from .config import Config

weatherKey = Config["weatherKey"]
googlekey = os.getenv("GOOGLE_API_KEY")


script_path = os.path.dirname(os.path.abspath(__file__ + "/../"))

model = joblib.load(script_path + "/saved_model/model.sav")


def call_google(origin, destination, googlekey):
    PARAMS = {
        "origin": origin,
        "destination": destination,
        "key": googlekey,
    }
    URL = "https://maps.googleapis.com/maps/api/directions/json"
    res = requests.get(url=URL, params=PARAMS)
    data = res.json()
    print(data, "2")
    # parse json to retrieve all lat-lng
    waypoints = data["routes"][0]["legs"]

    lats = []
    longs = []
    google_count_lat_long = 0

    # find cluster of interest from google api route
    for leg in waypoints:
        for step in leg["steps"]:
            start_loc = step["start_location"]
            lats.append(start_loc["lat"])
            longs.append(start_loc["lng"])
            google_count_lat_long += 1

    lats = tuple(lats)
    longs = tuple(longs)
    print("total waypoints: " + str(google_count_lat_long))

    return lats, longs, google_count_lat_long


def calc_distance(accident_dataset, lats, longs, google_count_lat_long):
    # load all cluster accident waypoints to check against proximity
    accident_point_counts = len(accident_dataset.index)

    # approximate radius of earth in km
    R = 6373.0
    # repeat data frame (9746*waypoints_count) times
    new = accident_dataset.append(
        [accident_dataset] * (google_count_lat_long - 1), ignore_index=True
    )
    lats_r = list(
        itertools.chain.from_iterable(
            itertools.repeat(x, accident_point_counts) for x in lats
        )
    )
    longs_r = list(
        itertools.chain.from_iterable(
            itertools.repeat(x, accident_point_counts) for x in longs
        )
    )
    new["lat2"] = np.radians(lats_r)
    new["long2"] = np.radians(longs_r)
    new["lat1"] = np.radians(new["Latitude"])
    new["long1"] = np.radians(new["Longitude"])
    new["dlon"] = new["long2"] - new["long1"]
    new["dlat"] = new["lat2"] - new["lat1"]

    new["a"] = (
        np.sin(new["dlat"] / 2) ** 2
        + np.cos(new["lat1"]) * np.cos(new["lat2"]) * np.sin(new["dlon"] / 2) ** 2
    )
    new["distance"] = R * (2 * np.arctan2(np.sqrt(new["a"]), np.sqrt(1 - new["a"])))

    return new


def call_weatherapi(place, weatherKey):
    api_to_model = {
        "temperature": "Temperature(F)",
        "feelslike": "Wind_Chill(F)",
        "humidity": "Humidity(%)",
        "visibility": "Visibility(mi)",
        "wind_speed": "Wind_Speed(mph)",
        "precip": "Preciptation(in)",
        "weather_code": "Weather_Condition",
        # "is_day": "Sunrise_Sunset"
    }
    # weather api call
    weather = pd.DataFrame()

    # time format for darksky API, eg 2019-04-11T23:00:00
    # datetime_str = datetime.datetime.strptime(
    #     tm, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%dT%H:%M')

    weather_url = (
        f"http://api.weatherstack.com/current?access_key={weatherKey}&query={place}"
    )
    w_response = requests.get(weather_url)
    w_data = w_response.json()
    print(w_data, 3)

    weather_data_for_model = {}
    for key, val in api_to_model.items():
        weather_data_for_model[val] = w_data["current"][key]

    weather_data_for_model["Sunrise_Sunset"] = (
        0 if w_data["current"]["is_day"] == "yes" else 1
    )
    # put json into a dataframe
    # datetime_object = datetime.datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    iweather = pd.DataFrame(weather_data_for_model, index=[0])
    # iweather["Cluster"] = row['Cluster']
    # iweather['precipAccumulation'] = 0

    weather = weather.append(iweather)
    return weather


def api_call(origin, origin_name):

    lat = origin.split(",")[0]
    long = origin.split(",")[1]

    weather = call_weatherapi(origin_name, weatherKey)
    # merge with accident data - df with latlong and weather
    position = pd.DataFrame({"Start_Lat": [lat], "Start_Long": [long]})

    final_df = pd.concat([position, weather], axis=1)

    # run model predicition
    final = {}
    final["severity"] = int(model.predict(final_df).squeeze())

    return final

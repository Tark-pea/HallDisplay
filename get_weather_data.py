#!/usr/bin/env python3
import requests

LAT = 35.727
LON = -81.686

headers = {
    "User-Agent": "HallDisplay/1.0 (braydon@example.com)",
    "Accept": "application/geo+json"
}

def get_forecast():
    points_url = f"https://api.weather.gov/points/{LAT},{LON}"
    points_resp = requests.get(points_url, headers=headers, timeout=10)
    points_resp.raise_for_status()
    points_data = points_resp.json()

    forecast_url = points_data["properties"]["forecast"]
    forecast_resp = requests.get(forecast_url, headers=headers, timeout=10)
    forecast_resp.raise_for_status()
    forecast_data = forecast_resp.json()

    periods = forecast_data["properties"]["periods"]

    for period in periods[:1]:
#        print(period["name"])
        today = (period["temperature"], period["temperatureUnit"])
        today = str(today[0]) + "°F \n" +str(period["shortForecast"])
        return today	        


if __name__ == "__main__":
    print(get_forecast())

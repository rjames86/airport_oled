from threading import local
import xml.etree.ElementTree as ET
import requests
from dateutil import parser
from dateutil.tz import gettz
import datetime
import json


class AirportData:
    URL = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1.5&stationString="
    METAR_TAGS = [
        "altim_in_hg",
        "dewpoint_c",
        "elevation_m",
        "flight_category",
        "latitude",
        "longitude",
        "maxT_c",
        "metar_type",
        "minT_c",
        "observation_time",
        "sea_level_pressure_mb",
        "station_id",
        "temp_c",
        "visibility_statute_mi",
        "wind_dir_degrees",
        "wind_speed_kt",
    ]

    READABLE_NAMES = dict(
        dewpoint_c="Dewpoint",
        elevation_m="Elevation",
        flight_category="Category",
        latitude="Latitude",
        longitude="Longitude",
        maxT_c="Max Temp",
        metar_type="Metar Type",
        minT_c="Min Temp",
        observation_time="Time",
        sea_level_pressure_mb="Pressure",
        station_id="Station ID",
        temp_c="Temp",
        visibility_statute_mi="Visibility",
        wind_dir_degrees="Wind Direction",
        wind_speed_kt="Wind Speed",
        wind_and_speed="Wind/Speed",
        sea_level_pressure_hg="Pressure (Hg)",
    )

    TIMEZONE = "America/Denver"

    def __init__(self):
        self.airport_code = "KMSO"
        self.last_run = datetime.datetime.now(tz=gettz("America/Denver"))

        self._data = None

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def wind_and_speed(self):
        return "%sº @ %s kt/hr" % (self.wind_dir_degrees, self.wind_speed_kt)

    @property
    def altim_in_hg(self):
        return self.data.get("altim_in_hg")

    @property
    def dewpoint_c(self):
        return self.data.get("dewpoint_c")

    @property
    def elevation_m(self):
        return self.data.get("elevation_m")

    @property
    def flight_category(self):
        return self.data.get("flight_category")

    @property
    def latitude(self):
        return self.data.get("latitude")

    @property
    def longitude(self):
        return self.data.get("longitude")

    @property
    def maxT_c(self):
        return self.data.get("maxT_c")

    @property
    def metar_type(self):
        return self.data.get("metar_type")

    @property
    def minT_c(self):
        return self.data.get("minT_c")

    @property
    def observation_time(self):
        time_data = self.data.get("observation_time")
        if time_data:
            dt = parser.parse(time_data)
            local_dt = dt.astimezone(gettz(self.TIMEZONE))
            return local_dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None

    @property
    def sea_level_pressure_mb(self):
        return self.data.get("sea_level_pressure_mb")

    @property
    def sea_level_pressure_hg(self):
        return "%s Hg" % float(self.data.get("sea_level_pressure_mb")) * 0.029530

    @property
    def station_id(self):
        return self.data.get("station_id")

    @property
    def temp_c(self):
        return "%sº C" % self.data.get("temp_c")

    @property
    def visibility_statute_mi(self):
        return self.data.get("visibility_statute_mi")

    @property
    def wind_dir_degrees(self):
        return self.data.get("wind_dir_degrees")

    @property
    def wind_speed_kt(self):
        return self.data.get("wind_speed_kt")

    @property
    def data(self):
        if self._data is None:
            results = []
            root = ET.fromstring(self.get_content())
            for metar in root.iter("METAR"):
                result = {}
                for child in metar:
                    if child.tag in self.METAR_TAGS:
                        result[child.tag] = child.text
                results.append(result)
            if len(results) > 0:
                self._data = results[0]
            else:
                self._data = {}
        return self._data

    def should_refresh(self):
        now = datetime.datetime.now(tz=gettz(self.TIMEZONE))
        delta = now - self.last_run
        if delta.total_seconds() / 60 > 1:
            self.last_run = datetime.datetime.now(tz=gettz("America/Denver"))
            self._data = None
            return True
        return False

    def get_content(self):
        print("Fetching fresh airport data...")
        return requests.get(self.URL + self.airport_code).content

    def write_json(self):
        with open("airport_data", "wb+") as f:
            json.dump(f, self.data)

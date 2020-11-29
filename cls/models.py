import requests

"""
api guide: https://openweathermap.org/current
weather conditions: https://openweathermap.org/weather-conditions

"""


class BaseModel:
    base_url = "http://api.openweathermap.org"
    _error_message = None
    _error_code = None

    def __init__(self, api_key=None, units="metric"):
        if not api_key:
            self.api_key = "bfe84e5c8cf418f96490f980266e4898"
        self.units = units

    @property
    def error_message(self):
        return self._error_message

    @property
    def error_code(self):
        return self._error_code

    def _fetch(self, url, *kwargs):
        r = requests.get(url, *kwargs)
        res = r.json()
        if r.ok:
            self._error_code = None
            self._error_message = None
            return res
        else:
            self._error_message = res["message"]
            self._error_code = res["cod"]
            return False

    def _make_main_url(self, url):
        return self.base_url + url

    def _add_parameters(self, url, parameters):
        default_parameters = {"appid": self.api_key, "units": self.units}
        parameters.update(default_parameters)
        for key, val in parameters.items():
            url += f"{key}={val}&"
        return url


class CurrentWeather(BaseModel):
    current_weather_url = "/data/2.5/weather?"

    def current_weather_by_city(self, city):
        parameters = {"q": city}
        main_url = self._make_main_url(self.current_weather_url)
        main_url = self._add_parameters(main_url, parameters)
        return self._fetch(main_url)

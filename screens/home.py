from threading import Thread

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from cls.button import ClearButton
from cls.jsontool import JsonTool
from cls.models import CurrentWeather

Builder.load_string(
    """
#:import WeatherUI cls.weather_animations.WeatherUI

<Home>:
    name: "Home"
    summary:summary
    weather:weather

    AKSwipeMenu:
        id: swipe
        allow_swipe: False

        AKSwipeMenuMainContent:
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: weather._bg_color

                MDToolbar:
                    title: "Weather"
                    md_bg_color: 0,0,0,0
                    anchor_title: "center"
                    _hard_shadow_a : 0
                    _soft_shadow_a : 0
                    left_action_items: [("cog-outline", lambda x: app.show_screen("Setting"))]
                    right_action_items: [("dots-vertical", lambda x: None)]

                WeatherUI:
                    id: weather

                BoxLayout:
                    padding: dp(10)
                    orientation: "vertical"
                    spacing: dp(5)

                    canvas.before:
                        Color:
                            rgba: weather._bg_color
                        Rectangle:
                            pos: self.pos
                            size: self.size
                            source: "assets/dark_bg.png"

                    Summary:
                        id: summary

                    ClearButton:
                        text: "More details"
                        text_color: 0.1,5,0.4,1
                        height: dp(60)


        AKSwipeMenuTopContent:
            size_hint_y: None
            height: dp(50)
            ClearButton:
                text: "My Cities"
                height: dp(50)
                _no_ripple_effect: True
                on_release: swipe.open()

        AKSwipeMenuBottomContent:
            size_hint_y: None
            height: dp(300)

            ScrollView:
                SwipeCities:
                    id: swipecities

"""
)


class Home(Screen):
    summary = ObjectProperty()
    weather = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def add_city_swipe(self, city):
        self.ids.swipecities.add_widget(
            ClearButton(text=city, halign="left", on_release=self.city_callback)
        )

    def city_callback(self, instance):
        def get(*args):
            city = instance.text
            details = self.get_city_weather(city)
            self.summary.city = details["city"]
            self.summary.country = details["country"]
            self.summary.temp = details["temp"]
            self.summary.condition = details["description"].capitalize()
            icon = details["icon"]
            self.summary.icon = f"assets/{icon}.png"
            self.start_animation(details["description"], icon)
            self.app.spinner.dismiss()

        self.app.spinner.open()
        t = Thread(target=get)
        t.start()
        self.ids.swipe.dismiss()

    def get_city_weather(self, city):
        w = CurrentWeather()
        details = w.current_weather_by_city(city)
        if not details:
            print("failed ", w.error_message)
            return

        new_details = {}
        new_details["description"] = details["weather"][0]["description"]
        new_details["icon"] = details["weather"][0]["icon"]
        new_details["temp"] = str(int(details["main"]["temp"]))
        new_details["country"] = details["sys"]["country"]
        new_details["city"] = details["name"]
        return new_details

    def start_animation(self, des, icon):
        d_n = icon[-1]
        if des == "clear sky":
            self.weather.make_fine()
        elif des in ["few clouds", "scattered clouds", "broken clouds"]:
            self.weather.make_fine_cloudy()
        elif "rain" in des:
            self.weather.make_rain()
        elif des in ["thunderstorm", "mist"]:
            self.weather.make_cloudy()
        elif des in ["snow"]:
            print("snow")

        if d_n == "n":
            self.weather.make_night()
        elif d_n == "d":
            self.weather.make_day()

    def on_pre_enter(self, *args):
        j = JsonTool()
        cities = j.get_cities()
        self.ids.swipecities.clear_widgets()
        for c in cities:
            self.add_city_swipe(c)

        return super().on_pre_enter(*args)

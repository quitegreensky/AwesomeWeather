from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd_extensions.akivymd.uix.statusbarcolor import change_statusbar_color

Builder.load_string(
    """

<WeatherUI>:
    id: terrain
    size_hint_y: None
    height: dp(300)

    canvas:

        # =======================
        # Horizon gradient
        # =======================
        Color:
            rgba: root._bg_color
        Rectangle:
            pos: self.pos
            size: self.size
            source: "assets/grad.png"

        # =======================
        # Sun
        # =======================
        PushMatrix
        Rotate:
            origin : self.size[0]/2, self.y-dp(1500)
            angle: root._sun_angle
        Color:
            rgba: 1,1,1,1
            a : root._moon_sun_opacity
        Rectangle:
            size: root.moon_sun_size, root.moon_sun_size
            pos: 0 , self.pos[1]+ dp(120)
            source: "assets/sun.png"
        PopMatrix

        # =======================
        # Stars
        # =======================
        Color:
            rgba: 1,1,1,1
            a: root._stars_alpha
        Rectangle:
            size: self.size
            pos: self.pos
            source: "assets/stars.png"

        # =======================
        # Moon
        # =======================
        PushMatrix
        Rotate:
            origin : self.size[0]/2, self.y-dp(1500)
            angle: root._moon_angle
        Color:
            rgba: 1,1,1,1
            a : root._moon_sun_opacity
        Rectangle:
            size: root.moon_sun_size, root.moon_sun_size
            pos: 0 , self.pos[1]+ dp(120)
            source: "assets/moon.png"
        PopMatrix

        # =======================
        # Clouds
        # =======================
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.width - dp(180) , dp(120)
            pos: dp(180) , self.pos[1]+ root._cloud_y
            source: "assets/cloud.png"
        Rectangle:
            size: self.width - dp(180) , dp(120)
            pos: 0 , self.pos[1]+ root._cloud_y
            source: "assets/cloud.png"


        # =======================
        # Birds
        # =======================
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.width - dp(180) , dp(120)
            pos: dp(180) , self.pos[1]+ root._birds_y
            source: "assets/birds.png"

        # =======================
        # Rain
        # =======================
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.width - dp(150) , dp(150)
            pos: dp(150) , self.pos[1]+ root._rain_y
            source: "assets/rain.png"
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.width - dp(150) , dp(150)
            pos: 0 , self.pos[1]+ root._rain_y
            source: "assets/rain.png"

        # =======================
        # Ufo
        # =======================
        PushMatrix
        Rotate:
            origin : dp(285) , self.pos[1]+dp(285)
            angle: root._ufo_angle1
        Rotate:
            origin : dp(295) , self.pos[1]+dp(258)
            angle: root._ufo_angle2
        Color:
            rgba: 1,1,1,1
            a: root._ufo_alpha
        Rectangle:
            size: dp(75), dp(50)
            pos: dp(250) , self.pos[1]+dp(200)
            source: "assets/ufo.png"
        PopMatrix

        # =======================
        # Mountains
        # =======================
        Color:
            rgba: root._bg_color
        Rectangle:
            pos: self.pos
            size: self.size
            source: "assets/mountain.png"
    """
)


class WeatherUI(BoxLayout):

    _bg_color = ListProperty([0, 0, 0, 0])
    moon_sun_size = NumericProperty("200dp")
    _sun_angle = NumericProperty(0)
    _moon_angle = NumericProperty(0)
    _cloud_y = NumericProperty(0)
    _rain_y = NumericProperty(0)
    _moon_sun_opacity = NumericProperty(1)
    _statusbar_color = ListProperty([0, 0, 0, 1])
    _birds_y = NumericProperty(0)
    _stars_alpha = NumericProperty(0)
    _ufo_angle1 = NumericProperty(0)
    _ufo_angle2 = NumericProperty(0)
    _ufo_alpha = NumericProperty(0)

    day_color = [129 / 255, 211 / 255, 249 / 255, 1]
    night_color = [0, 0, 0.7, 1]

    _day_night_state = "night"
    _weather_state = "fine"

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self._update)

    def _update(self, *args):
        self.make_day(anim=False)
        self.make_fine()

    def set_statusbar_color(self, color):
        (Animation(_statusbar_color=color)).start(self)

    def on__statusbar_color(self, *args):
        change_statusbar_color(args[1])

    def set_bg_state(self, state, anim=True):
        if state == "day":
            self.set_statusbar_color(self.day_color)
            if anim:
                anim = Animation(_bg_color=self.day_color)
            else:
                self._bg_color = self.day_color
                return

        elif state == "night":
            self.set_statusbar_color(self.night_color)
            if anim:
                anim = Animation(_bg_color=self.night_color)
            else:
                self._bg_color = self.night_color
                return
        anim.start(self)

    def set_ufo_state(self, state):
        if state == "show":
            anim = Animation(_ufo_angle1=360, _ufo_angle2=360)
            anim &= Animation(_ufo_alpha=1, d=0.5)
        elif state == "hide":
            anim = Animation(_ufo_angle1=0, _ufo_angle2=0)
            anim &= Animation(_ufo_alpha=0, d=0.5)
        anim.start(self)

    def set_moon_sun_state(self, state, anim=True):
        if state == "moon" and self._day_night_state == "day":
            self._moon_angle = 10
            anim = Animation(_sun_angle=-55)
            anim &= Animation(_moon_angle=0)
        elif state == "sun" and self._day_night_state == "night":
            self._sun_angle = 10
            anim = Animation(_moon_angle=-55)
            anim &= Animation(_sun_angle=0)
        else:
            return
        anim.start(self)

    def set_stars_state(self, state):
        if state == "show":
            anim = Animation(_stars_alpha=1, t="out_quad", d=0.5)
            self.set_ufo_state("show")
        elif state == "hide":
            anim = Animation(_stars_alpha=0, t="out_quad", d=0.5)
            self.set_ufo_state("hide")
        anim.start(self)

    def set_cloud_state(self, state):
        if state == "show":
            anim = Animation(_cloud_y=dp(200), t="out_elastic")
        elif state == "hide":
            anim = Animation(_cloud_y=-dp(30), t="in_elastic")
        anim.start(self)

    def set_rain_state(self, state):
        if state == "show":
            anim = Animation(_rain_y=dp(90), t="in_out_back")
        elif state == "hide":
            anim = Animation(_rain_y=-dp(40), t="in_out_back")
        anim.start(self)

    def set_moon_sun_show(self, state):
        if state == "show":
            anim = Animation(_moon_sun_opacity=1, d=0.5, t="out_quad")
        elif state == "hide":
            anim = Animation(_moon_sun_opacity=0, d=0.5, t="out_quad")
        anim.start(self)

    def set_birds_state(self, state):
        if state == "show":
            anim = Animation(_birds_y=dp(200), d=0.5, t="out_quad")
        elif state == "hide":
            anim = Animation(_birds_y=-dp(30), d=0.5, t="out_quad")
        anim.start(self)

    def make_night(self):
        self.set_moon_sun_state("moon")
        self.set_bg_state("night")
        self._day_night_state = "night"
        self.set_birds_state("hide")

        if self._weather_state in ["fine", "fine_cloudy"]:
            self.set_stars_state("show")
        else:
            self.set_stars_state("hide")

    def make_day(self, anim=True):
        self.set_moon_sun_state("sun", anim=anim)
        self.set_bg_state("day", anim=anim)
        self._day_night_state = "day"
        self.set_stars_state("hide")

        if self._weather_state in ["fine", "fine_cloudy"]:
            self.set_birds_state("show")
        else:
            self.set_birds_state("hide")

    def make_fine_cloudy(self):
        self.set_moon_sun_show("show")
        self.set_cloud_state("show")
        self.set_rain_state("hide")

        if self._day_night_state == "night":
            self.set_stars_state("show")
            self.set_birds_state("hide")
        else:
            self.set_stars_state("hide")
            self.set_birds_state("show")
        self._weather_state = "fine_cloudy"

    def make_fine(self):
        self.set_moon_sun_show("show")
        self.set_cloud_state("hide")
        self.set_rain_state("hide")

        if self._day_night_state == "day":
            self.set_birds_state("show")
            self.set_stars_state("hide")
        else:
            self.set_stars_state("show")
            self.set_birds_state("hide")
        self._weather_state = "fine"

    def make_rain(self):
        self.set_moon_sun_show("hide")
        self.set_cloud_state("show")
        self.set_rain_state("show")
        self.set_birds_state("hide")
        self.set_stars_state("hide")
        self._weather_state = "rain"

    def make_cloudy(self):
        self.set_moon_sun_show("hide")
        self.set_cloud_state("show")
        self.set_rain_state("hide")
        self.set_birds_state("hide")
        self.set_stars_state("hide")
        self._weather_state = "cloudy"

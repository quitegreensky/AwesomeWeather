from os import path

from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel

Builder.load_string(
    """
<MyLabel>:
    valign: "center"
    halign: "center"
    theme_text_color: "Custom"
    text_color: 1,1,1,1

"""
)


class MyLabel(MDLabel):
    myfont = StringProperty("regular")

    fonts_path = "fonts/"
    fonts_def = {"regular": "KozGoPro-Regular.otf", "light": "KozGoPro-ExtraLight.otf"}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._update)

    def _update(self, *args):
        font_path = path.join(self.fonts_path, self.fonts_def[self.myfont])
        self.font_name = font_path

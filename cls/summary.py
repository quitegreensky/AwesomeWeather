from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_string(
    """

<Summary>
    orientation: "vertical"
    spacing: dp(10)
    size_hint_y: None
    height: self.minimum_height

    BoxLayout:
        id: icon
        size_hint_y: None
        height: dp(80)
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: self.size[0]/2 - dp(20) , self.pos[1]
                size: self.height, self.height
                source: root.icon

    MyLabel:
        text: root.city+ ", "+ root.country
        font_size: dp(30)
        adaptive_height: True

    MyLabel:
        text: root.condition
        myfont: "light"
        font_size: dp(20)
        adaptive_height: True

    MyLabel:
        text: "Temperature: "+ root.temp + u"\N{DEGREE SIGN}C"
        myfont: "light"
        font_size: dp(20)
        adaptive_height: True


"""
)


class Summary(BoxLayout):
    temp = StringProperty("-")
    condition = StringProperty("-")
    city = StringProperty("-")
    country = StringProperty("-")
    icon = StringProperty("assets/10d.png")

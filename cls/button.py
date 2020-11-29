from kivy.lang.builder import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import RectangularRippleBehavior

from cls.label import MyLabel

Builder.load_string(
    """
<CircularIcon@BoxLayout>
    bg_color: 0,0,0,1
    icon: ''
    canvas.before:
        Color:
            rgba: root.bg_color
        Ellipse:
            pos: self.pos
            size: self.size
    MDIcon:
        icon: root.icon
        halign: "center"
        valign: "center"
        theme_text_color: "Custom"
        text_color: 1,1,1,1

<ClearButton>
    size_hint_y: None
    height: dp(40)
    padding: [dp(10), 0]
    radius : [dp(10),]

<IconListItem>:

    size_hint_y: None
    height: dp(40)
    spacing: dp(10)
    CircularIcon:
        size_hint_x: None
        width: root.height
        icon: root.icon
        bg_color: root.bg_color

    MyLabel:
        text: root.text
        halign: "left"
        font_size: dp(15)

    MDIconButton:
        id: remove_but
        icon: "delete"
        theme_text_color: "Custom"
        text_color: 1,1,1,1

    """
)


class ClearButton(ButtonBehavior, RectangularRippleBehavior, MyLabel):
    pass


class IconListItem(ButtonBehavior, BoxLayout):
    icon = StringProperty("map-marker-circle")
    text = StringProperty("")
    bg_color = ListProperty([0.5, 0, 50, 0.2, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.ids.remove_but.collide_point(*touch.pos):
            return super().on_touch_up(touch)
        else:
            return True

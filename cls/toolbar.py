from kivy.event import EventDispatcher
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

Builder.load_string(
    """
<MyToolbar>
    size_hint_y: None
    height: dp(50)

    MDIconButton:
        id: but
        icon: root.icon
        theme_text_color: "Custom"
        text_color: 1,1,1,1
        pos_hint: {"center_y": .5}
        x: dp(5)
        on_release: root.dispatch("on_release", self)

    MyLabel:
        text: root.text

    """
)


class MyToolbar(MDRelativeLayout, EventDispatcher):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.register_event_type("on_release")

    def on_release(self, *args):
        pass

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string(
    """
<SwipeCities>
    padding: dp(10)
    orientation: "vertical"
    adaptive_height: True

    """
)


class SwipeCities(MDBoxLayout):
    pass

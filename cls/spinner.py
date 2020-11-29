from kivy.lang.builder import Builder
from kivymd.uix.dialog import BaseDialog

Builder.load_string(
    """
<MySpinner>
    auto_dismiss: False
    size_hint: None, None
    size: dp(100), dp(100)

    AKSpinnerCircleFlip:
        id: spinner
        spinner_size: dp(90)
        pos_hint: {"center_x": .5,  "center_y": .5}

"""
)


class MySpinner(BaseDialog):
    def on_open(self):
        self.ids.spinner.active = True
        return super().on_open()

    def on_dismiss(self):
        self.ids.spinner.active = False
        return super().on_dismiss()

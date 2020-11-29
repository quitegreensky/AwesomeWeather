import kivymd_extensions.akivymd  # noqa
from kivy.factory import Factory  # noqa
from kivy.lang.builder import Builder
from kivymd.app import MDApp

import cls.factory  # noqa
from cls.spinner import MySpinner

KV = """

ScreenManager:

"""


class Main(MDApp):
    def build(self):
        self.mainkv = Builder.load_string(KV)
        return self.mainkv

    def on_start(self):
        self.spinner = MySpinner()
        self.show_screen("Home")

    def show_screen(self, name, mode="forward"):
        self.load_string(name)

        if mode == "back":
            self.mainkv.transition.direction = "left"
        else:
            self.mainkv.transition.direction = "right"
        self.mainkv.transition.duration = 0.3
        self.mainkv.current = name

    def load_string(self, name):
        if not self.mainkv.has_screen(name):
            exec("from screens import %s" % name.lower())
            self.mainkv.add_widget(eval("Factory.%s()" % name))

    def get_screen(self, name):
        return self.mainkv.get_screen(name)


if __name__ == "__main__":
    Main().run()

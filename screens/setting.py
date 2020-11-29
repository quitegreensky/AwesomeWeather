import json

from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

from cls.jsontool import JsonTool

Builder.load_string(
    """
<MyAddBox@MDBoxLayout+AKAddWidgetAnimationBehavior>

<AddDialogContent>:
    orientation: "vertical"
    padding: dp(10)
    MDTextField:
        hint_text: "Your city"
        on_text: root.search_city(self.text)

    ScrollView:
        MyAddBox:
            adaptive_height: True
            id: scroll
            orientation: "vertical"

<Setting>
    name: "Setting"

    MDBoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba:app.get_screen("Home").weather._bg_color
            Rectangle:
                pos: self.pos
                size: self.size
                source: "assets/dark_bg.png"

        MDToolbar:
            title: "Settings"
            md_bg_color: 0,0,0,0
            left_action_items: [\
                ("chevron-left", lambda x: app.show_screen("Home", "back"))\
                    ]

        ScrollView:
            MyAddBox:
                id: scroll
                padding: dp(20)
                orientation: "vertical"
                adaptive_height: True


    AKFloatingRoundedAppbar:
        press_effect: False
        AKFloatingRoundedAppbarButtonItem:
            icon: "plus"
            text: "Add"
            on_release: root.add_dialog()


    """
)


class AddDialogContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def search_city(self, city):
        self.ids.scroll.clear_widgets()
        if len(city) <= 3:
            return

        cities_found = []
        with open("assets/cities.json") as f:
            js = json.load(f)
            cities = js["cities"]

            for c in cities:
                if city in c.lower():
                    widget = OneLineListItem(text=c, on_release=self.add_city)
                    cities_found.append(widget)

            self.ids.scroll.items = cities_found

    def add_city(self, instance):
        j = JsonTool()
        j.add_city(instance.text)
        self.parent.parent.parent.dismiss()


class Setting(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def add_dialog(self):
        dialog = AKAlertDialog(
            fixed_orientation="portrait",
            header_icon="map-marker-outline",
            header_height_portrait="90dp",
            size_portrait=["250dp", "500dp"],
            auto_dismiss=True,
        )
        dialog.content_cls = Factory.AddDialogContent()
        dialog.bind(on_dismiss=self.load_cities)
        dialog.open()

    def load_cities(self, *args):
        j = JsonTool()
        cities = j.get_cities()
        self.ids.scroll.clear_widgets

        cities_widget = []
        for c in cities:
            widget = Factory.IconListItem(text=c, on_release=self.remove_city)
            cities_widget.append(widget)
        self.ids.scroll.items = cities_widget

    def on_pre_enter(self, *args):
        self.load_cities()
        return super().on_pre_enter(*args)

    def remove_city(self, instance):
        JsonTool().remove_city(instance.text)
        self.load_cities()

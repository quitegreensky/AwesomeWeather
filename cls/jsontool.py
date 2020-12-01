import json
from os import pardir, path


class JsonTool:
    main_path = path.join(path.dirname(__file__), pardir, "mycities.json")

    def new(self, js=None):
        if not js:
            js = {"cities": []}
        with open(self.main_path, "wt") as f:
            json.dump(js, f)

    def open(self):
        if not self.exists():
            self.new()
        with open(self.main_path) as f:
            j = json.load(f)
            return j

    def exists(self):
        if path.exists(self.main_path):
            return True
        else:
            return False

    def get_cities(self):
        return self.open()["cities"]

    def add_city(self, city):
        js = self.open()
        js["cities"].append(city)
        self.new(js)

    def remove_city(self, city):
        js = self.open()
        cities = js["cities"]
        new_cities = [x for x in cities if x != city]
        js["cities"] = new_cities
        self.new(js)

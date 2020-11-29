from kivy.factory import Factory

r = Factory.register
r("MyLabel", module="cls.label")
r("Summary", module="cls.summary")
r("ClearButton", module="cls.button")
r("SwipeCities", module="cls.swipecities")
r("IconListItem", module="cls.button")

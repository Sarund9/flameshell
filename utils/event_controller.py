

from gi.repository import Gtk  # type: ignore
from ignis.base_widget import BaseWidget
from ignis import utils

from ignis.gobject import IgnisProperty, IgnisSignal



# class EventController(Gtk.EventControllerKey, BaseWidget):
#     __gtype_name__ = "IgnisEventController"
#     __gproperties__ = {**BaseWidget.gproperties}

#     def __init__(
#         self,

#         **kwargs,
#     ):
#         Gtk.EventController.__init__(self, application=app)

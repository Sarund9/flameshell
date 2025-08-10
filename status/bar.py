
import sys
import os
import os.path as osp
import datetime

# import gi.widgets as gw # type: ignore
# from gi.repository import Gtk # type: ignore
# from gi.repository import Graphene # type: ignore

from ignis import utils
import ignis
from ignis.widgets import Widget
from ignis.utils import Utils

from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.app import IgnisApp

from .center import StatusCenter

from .pad import StatusClock

network = NetworkService.get_default()


class Bar(Widget.Window):
    __gtype_name__ = "Bar"
    def __init__(self, monitor: int):
        # self._center = StatusCenter(monitor)

        # TODO: Better device selection..
        for dev in network.wifi.devices:
            self._wifi = WifiStatus(dev)
            break

        super().__init__(
            anchor=[ "left", "bottom", "right" ],
            exclusivity="exclusive",
            monitor=monitor,
            namespace=f"bar-{monitor}",
            layer="top",
            kb_mode="none",
            child=Widget.CenterBox(
                # end_widget=Widget.EventBox(
                #     vertical=False,
                #     child=[self._wifi, Clock()],
                #     on_click=lambda x: self._center.toggle(),
                #     css_classes=["status"],
                # ),
                end_widget=Widget.Box(
                    child=[StatusClock(monitor)]
                )
            ),
            css_classes=["bar"],
        )

class Clock(Widget.Box):
    time: Widget.Label
    date: Widget.Label

    def __init__(self):
        self.time = Widget.Label(
                    css_classes=["time"],
                    label = ""
                    )
        self.date = Widget.Label(
                    css_classes=["date"],
                    label = ""
                    )
        Utils.Poll(
            1_000, self.update
        )
        super().__init__(
            css_classes=["clock", ""],
            vertical=True,
            spacing=0,
            child=[self.time, self.date]
        )

    def update(self, a):
        now = datetime.datetime.now()
        self.time.set_label(now.strftime("%H:%M"))
        self.date.set_label(now.strftime("%d %b %Y"))

class WifiStatus(Widget.CenterBox):
    def __init__(self, device: WifiDevice):
        def get_icon(icon_name: str) -> str:
            if device.ap.is_connected:
                return icon_name
            else:
                return "network-wireless-symbolic"

        super().__init__(
            css_classes=["status-wifi"],
            vertical=True,
            center_widget=Widget.Icon(
                image=device.ap.bind("icon-name", get_icon),
                pixel_size=30,
                )
        )



import sys
import os
import os.path as osp
import datetime

# import gi.widgets as gw # type: ignore
# from gi.repository import Gtk # type: ignore
# from gi.repository import Graphene # type: ignore

from ignis import utils
import ignis
from ignis.widgets import *
from ignis.utils import Utils

from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.app import IgnisApp

from .pad import Pad, ControlCenter

network = NetworkService.get_default()


class Bar(Window):
    __gtype_name__ = "Bar"
    def __init__(self, monitor: int):
        # self._center = StatusCenter(monitor)

        # TODO: Better device selection..
        for dev in network.wifi.devices:
            self._wifi = WifiStatus(dev)
            break

        left: list[Pad] = [
            
        ]
        center: list[Pad] = [

        ]
        right: list[Pad] = [
            ControlCenter(monitor),
        ]
        # for pad in left:
        #     pad.initialize(monitor)
        # for pad in center:
        #     pad.initialize(monitor)
        # for pad in right:
        #     pad.initialize(monitor)

        super().__init__(
            anchor=[ "left", "top", "right" ],
            exclusivity="exclusive",
            monitor=monitor,
            namespace=f"bar-{monitor}",
            layer="top",
            kb_mode="none",
            child=CenterBox(
                start_widget=Box(
                    child=left,
                ),
                center_widget=Box(
                    child=center,
                ),
                end_widget=Box(
                    child=right,
                ),
            ),
            css_classes=["bar"],
        )

class Clock(Box):
    time: Label
    date: Label

    def __init__(self):
        self.time = Label(
                    css_classes=["time"],
                    label = ""
                    )
        self.date = Label(
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

class WifiStatus(CenterBox):
    def __init__(self, device: WifiDevice):
        def get_icon(icon_name: str) -> str:
            if device.ap.is_connected:
                return icon_name
            else:
                return "network-wireless-symbolic"

        super().__init__(
            css_classes=["status-wifi"],
            vertical=True,
            center_widget=Icon(
                image=device.ap.bind("icon-name", get_icon),
                pixel_size=30,
                )
        )


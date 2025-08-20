
from ignis.widgets import *

from ignis.base_widget import GObject, BaseWidget
from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal
# from ignis.services.mpris import MprisService, MprisPlayer
# from ignis.services.audio import AudioService
from ignis.services.network import (
    NetworkService, Wifi, WifiAccessPoint, WifiDevice
)

network = NetworkService.get_default()

class Pill(EventBox):
    def __init__(
        self, *,
        image: str, label: str, menu: BaseWidget | None = None,
        **kwargs,
    ):

        # self._menu: PopoverMenu = menu

        pixel_size = 28

        super().__init__(
            hexpand=True,
            child=[
                Icon(pixel_size, image=image),
                Label(label=label),
                Icon(26, image='arrow-right-symbolic'),
                
                # ArrowButton(
                #     Arrow(pixel_size=pixel_size),
                #     halign="end",
                #     on_click=lambda x: self._revealer.toggle,
                # ) if menu is not None else None,
            ],
            on_right_click=self._clicked,
            **kwargs,
        )

    def _clicked(self, x):
        print("MENU")
        # if not self._menu:
        #     return
        
        # self._menu.popup()
    


def pill_wifi() -> Pill:

    # network-wireless-signal-excellent
    # network-wireless-signal-excellent-secure-symbolic
    # network-wireless-signal-good
    # network-wireless-signal-good-secure-symbolic
    # network-wireless-signal

    device: WifiDevice
    for dev in network.wifi.devices:
        device = dev
        break

    def get_label(ssid: str) -> str:
        if ssid:
            return ssid
        else:
            return "Wi-Fi"

    def get_icon(icon_name: str) -> str:
        if device.ap.is_connected:
            return icon_name
        else:
            return "network-wireless-symbolic"

    return Pill(
        label=device.ap.bind('ssid', get_label),
        image=device.ap.bind('icon-name', get_icon),
        # menu=PopoverMenu(
        #     items=[
        #         MenuItem(label='current network')
        #     ],
        # ),
    )



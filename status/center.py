


import ignis
from ignis.widgets import Widget


class StatusCenter(Widget.RevealerWindow):
    __gtype_name__ = "StatusCenter"
    def __init__(self, monitor: int):
        self._revealer = Widget.Revealer(
            transition_type='crossfade',
            transition_duration=95,
            reveal_child=True,
            child=Widget.Box(
                vertical=True,
                css_classes=["status-center"],
                child=[
                    Widget.Label(label="Wifi"),
                    Widget.Label(label="Bluetooth"),
                ]
            )
        )

        super().__init__(
            revealer=self._revealer,
            anchor=[ "bottom", "right" ],
            exclusivity="exclusive",
            monitor=monitor,
            namespace=f"status-center-{monitor}",
            layer="top",
            kb_mode="none",
            child=Widget.Box(
                child=[self._revealer]
            ),
            css_classes=["status-center-window"],
        )



    def toggle(self):
        self._revealer.toggle()



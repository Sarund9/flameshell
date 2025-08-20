

import ignis
from ignis.widgets import *

from ignis.base_widget import GObject, BaseWidget
from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal


class Pad(EventBox):
    def __init__(
        self,
        namespace:  str,
        anchor:     list[str],
        child:      list[BaseWidget],
        **kwargs,
    ):
        self._namespace  = namespace
        self._anchor     = anchor

        super().__init__(
            css_classes=['status-pad'],
            child=child,
            **kwargs,
        )
    
    def make_window(
        self, monitor: int, menu: BaseWidget, *,
        transition_type: str = 'crossfade',
        transition_duration: int = 100,
    ) -> RevealerWindow:
        revealer = Revealer(
            transition_type=transition_type,
            transition_duration=transition_duration,
            child=menu,
        )
        return RevealerWindow(
            css_classes=[],
            revealer=revealer,
            monitor=monitor,
            visible=False,
            anchor=self._anchor,
            popup=True,
            kb_mode="exclusive",
            layer="overlay",
            # exclusivity='exclusive',
            namespace=f"flameshell-pad-{self._namespace}-{monitor}",
            child=Box(
                child=[revealer],
            ),
        )


# class StatusPad(Widget.EventBox):
#     def __init__(self, name: str, monitor: int, menu: GObject, **kwargs):
#         self._window = StatusPadWindow(name, monitor, menu)

#         super().__init__(
#             on_click=lambda x: self._window.toggle(),
#             css_classes=["status-pad"],
#             **kwargs,
#         )

# class StatusPadWindow(Widget.RevealerWindow):
#     def __init__(self, name: str, monitor: int, menu: GObject):
#         self._revealer = Widget.Revealer(
#             transition_type='crossfade',
#             transition_duration=95,
#             reveal_child=True,
#             child=menu,
#             css_classes=["status-revealer"]
#             # child=Widget.Box(
#             #     vertical=True,
#             #     css_classes=[f"status-{name}", "status-revealer"],
#             #     child=child
#             # )
#         )
#         self.__gtype_name__ = f"status-{name}"

#         # self.toggle()

#         super().__init__(
#             revealer=self._revealer,
#             anchor=[ "bottom", "right" ],
#             exclusivity="exclusive",
#             monitor=monitor,
#             namespace=f"status-center-{monitor}",
#             layer="top",
#             kb_mode="none",
#             child=Widget.Box(
#                 child=[self._revealer]
#             ),
#             css_classes=[f"status-{name}", "status-window"],
#         )
    
#     def toggle(self):
#         self._revealer.toggle()


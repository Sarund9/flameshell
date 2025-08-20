

from ignis.widgets import *

from ignis.base_widget import GObject, BaseWidget
from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal
from ignis.services.mpris import MprisService, MprisPlayer
from ignis.services.audio import AudioService

from .pad import Pad

from .pills import (Pill, pill_wifi)


mpris: MprisService = MprisService.get_default()
audio: AudioService = AudioService.get_default()


class ControlCenterMenu(Box):
    def __init__(self):


        pills = [
            pill_wifi()
        ]

        pills = Grid(
            column_num=2,
            row_num=3,
            child=[
                pill_wifi(),
            ],
        )
        # pills = Stack(

        #     child=[
        #         StackPage('') for,
        #     ]
        # )

        volume_slider = self.volume()

        super().__init__(
            css_classes=['control-center'],
            vertical=True,
            child=[
                pills,
                volume_slider,
            ],
        )

    def volume(self) -> BaseWidget:
        rate = 0.7
        
        # md: 󰖁 󰕾 
        # fa:    

        def vol_text(vol: float) -> str:
            percent = vol / rate
            ico: str = ''
            if percent < 0.001:
                ico = ''
            if percent > 20:
                ico = ''
            if percent > 80:
                ico = ''

            return ico
        
        return Box(
            css_classes=['status-pad'],

            child=[
                Label(
                    label=audio.speaker.bind('volume', vol_text)
                ),
                Label(
                    width_request=70,
                    label=audio.speaker.bind('volume', lambda vol: f'{int(vol / rate)}%'),
                ),
                Scale(
                    css_classes=['status-pad'],
                    width_request=350,
                    min=0,
                    max=100,
                    step=1,
                    value=audio.speaker.bind('volume', lambda vol: vol / rate),
                    on_change=lambda x: audio.speaker.set_volume(x.value * rate),
                ),
            ]
        )


class ControlCenter(Pad):
    def __init__(self, monitor: int):

        def btn(child) -> Button:
            return Button(
                css_classes=['status-pad', 'control-center'],
                child=child,
            )

        super().__init__(
            namespace='control-center',
            anchor=['right', 'top'],
            child=[
                btn(Label(label='W')),
                btn(Label(label='B')),
                btn(Label(label='T')),
            ],

            on_click=self.toggle_window,
        )

        self._window = self.make_window(monitor, ControlCenterMenu(),
            transition_type='slide_left',
            transition_duration=220)

    def toggle_window(self, x):
        self._window.visible = not self._window.visible

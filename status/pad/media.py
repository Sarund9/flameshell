

from ignis.widgets import *

from ignis.base_widget import GObject, BaseWidget
from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal
from ignis.services.mpris import MprisService, MprisPlayer
from ignis.services.audio import AudioService

from .pad import Pad


mpris: MprisService = MprisService.get_default()
audio: AudioService = AudioService.get_default()


class MediaPlayer(Box):
    def __init__(self, player: MprisPlayer):
        self._player = player
        super().__init__(
            css_classes=['status-media-player'],
            vertical=True,
            child=[
                Box(
                    child=[
                        self.info(),
                        self.controls(),
                    ],
                ),
                Box(
                    child=[
                        self.slider(),
                        self.time(),
                    ],
                ),
            ],
        )
    
    def info(self):
        return Box(
            vertical=True,
            hexpand=True,
            halign='start',
            child=[
                Label(label='app'),
                Label(label='title'),
                Label(label='author'),
            ]
        )
    
    def controls(self):
        return Box(
            halign='end',
            vertical=True,
            child=[
                Button(child=Label(label='')),
                Box(
                    child=[
                        Button(child=Label(label='')),
                        Button(child=Label(label='')),
                    ]
                ),
            ]
        )
    
    def slider(self):
        return Scale(
            width_request=350,
            min=0,
            max=100,
            step=1,
            value=20,
            draw_value=True,
            value_pos='top',
        )
    
    def time(self):
        return Label(
            label=f'0:23/3:46'
        )


class MediaPad(Pad):
    def __init__(self, monitor: int):

        # Pause: 

        # mpris.connect('player_added', self.player_added)

        def btn(child) -> Button:
            return Button(
                css_classes=['status-pad', 'media-player'],
                child=child,
            )

        super().__init__(
            namespace='media',
            anchor=['left', 'top'],
            child=[
                btn(Label(label='')),
                btn(Label(label='')),
                btn(Label(label='')),
            ],

            on_middle_click=self.toggle_window,
        )

        self._window = self.make_window(monitor, self.menu())

    def toggle_window(self, x):
        self._window.visible = not self._window.visible

    def player_added(self, x):
        pass

    # def player(self, player: MprisPlayer) -> BaseWidget:

    #     return Label(
    #         css_classes=['status-media-player'],
    #         label=player.title,
    #     )

    def volume(self) -> BaseWidget:
        rate = 0.7
        return Scale(
            css_classes=['status-pad'],
            width_request=350,
            min=0,
            max=100,
            step=1,
            value=audio.speaker.bind('volume', lambda vol: vol / rate),
            on_change=lambda x: audio.speaker.set_volume(x.value * rate),

            # value=audio.sink.bind('volume', lambda value: int(value * 100)),
            # draw_value=True,
            # value_pos='top',
        )

    def menu(self) -> BaseWidget:
        def players_binding(players: list[MprisPlayer]) -> list[MediaPlayer]:
            if len(players) > 0:
                return [StackPage(p.identity, child=MediaPlayer(p)) for p in players]
            # for player in players:
            #     mp = MediaPlayer(player)
            #     page = StackPage(player.identity, mp)
            #     yield page

            # return []
        
        playerstack = Stack(
            child=mpris.bind('players', players_binding)
        )

        switcher = Box(

            child=playerstack.bind('child', lambda pages:
                [Icon(12, icon='circle') for page in pages]),
        )

        return Box(
            hexpand=True,
            vexpand=True,

            css_classes=['status-pad', 'media-player-box'],
            vertical=True,
            child=[
                self.volume(),
                EventBox(

                    child=[
                        switcher,
                        playerstack,
                    ],
                ),
                Label(label=mpris.bind('players', lambda pls: f"P: {len(pls)}"))
            ],
        )



import sys
import os
import os.path as osp
import datetime
import time

from typing import Any

# import gi.widgets as gw # type: ignore
from gi.repository import Gtk # type: ignore
from gi.repository import Graphene # type: ignore

from ignis import utils
import ignis
from ignis.widgets import *
from ignis.utils import Utils
from ignis.utils import monitor, icon
from ignis.services.applications import ApplicationsService, Application, application

from ignis.app import IgnisApp

from status import Bar

# from .switcher import Compositor
from utils import WayfireService, WayfireWindow

from wm import Workspace
from frame import Hotbar

wayfire = WayfireService.get_default()

def bind(binding: str, callback: callable):
    wayfire.register_binding(binding, mode='normal', exec_always=True, callback=callback)

def main():
    app = IgnisApp.get_default()
    app_dir = osp.dirname(osp.abspath(__file__))
    app.apply_css(osp.join(app_dir, 'style.scss'))

    work = Workspace()

    bind('<super> KEY_Q', work.left)
    bind('<super> KEY_W', work.right)
    bind('<super> KEY_SPACE', work.grab)
    
    hotbars = []

    for i in range(monitor.get_n_monitors()):
        Bar(i)
        hotbars.append(Hotbar(i, work))
    
    # def show():
    #     for hb in hotbars:
    #         hb.show()

    def show():
        work.shown_set(not work.shown)
        # print("Show")

    bind('<super> KEY_TAB', show)
    # bind('KEY_LEFTMETA', show)

    wayfire.begin_listening()

    work.right()
    # time.sleep(1.5)

    # for hb in hotbars:
    #     hb.set_visible(False)


class Debug(RegularWindow):
    __gtype_name__ = "DebugWindow"
    def __init__(self, monitor: int):


        super().__init__(
            css_classes=[],
            child=self.build(),
            namespace=f"debug-window-{monitor}",
            title="Debug",
            titlebar=HeaderBar(show_title_buttons=True),
        )

    def desc(self, win: WayfireWindow):
        return Label(
            label=win.bind("title")
        )
    
    def build(self):
        return Box(
            vertical=True,
            child=serv.bind('windows', lambda wins: [self.desc(w) for w in wins])
        )




main()


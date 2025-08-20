
import sys
import os
import os.path as osp
import datetime
import time

from typing import Any
from dataclasses import dataclass

# import gi.widgets as gw # type: ignore
from gi.repository import Gtk # type: ignore
from gi.repository import Graphene # type: ignore

from ignis import utils
import ignis
from ignis.widgets import *
from ignis.utils import Utils
from ignis.utils import monitor, icon
from ignis.services.applications import ApplicationsService, Application, application
from ignis.variable import Variable

from ignis.app import IgnisApp

from status import Bar

# from .switcher import Compositor
from utils import WayfireService, WayfireWindow

from wm import Workspace
from frame import Hotbar

wayfire = WayfireService.get_default()

def bind(binding: str, callback: callable):
    # NOTE: callback takes no Arguments
    wayfire.register_binding(binding, mode='normal', exec_always=True, callback=callback)

@dataclass
class TagBinding:
    num: int
    workspace: Workspace

    def exec(self):
        # print("Pressed:", self.num)
        self.workspace.toggle_tag(self.num)

def main():
    app = IgnisApp.get_default()
    app_dir = osp.dirname(osp.abspath(__file__))
    app.apply_css(osp.join(app_dir, 'style.scss'))

    work = Workspace()

    bind('<super> KEY_Q', work.left)
    bind('<super> KEY_W', work.right)
    bind('<super> KEY_SPACE', work.grab)
    # Tag bindings
    for i in range(1, 10):
        bind(f'<super> KEY_{i}', TagBinding(i, work).exec)

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


class Debug(Window):
    __gtype_name__ = "DebugWindow"
    def __init__(self, monitor: int):
        self._theme: Gtk.IconTheme

        self._list: list[str] = []

        super().__init__(
            css_classes=['debug'],
            child=self.build(),
            anchor=['left', 'bottom'],
            kb_mode='on_demand',
            margin_bottom=15,
            margin_left=10,
            layer='bottom',
            # dynamic_input_region=True,
            namespace=f"flameshell-debug-{monitor}",
            title="Debug",
            # titlebar=HeaderBar(show_title_buttons=True),
        )
        display = Gtk.Widget.get_display(self)

        itheme = Gtk.IconTheme.get_for_display(display)

        items = itheme.get_icon_names()
        # print(li)
        # self._theme = itheme
        self._list = [i for i in items]


    def desc(self, win: WayfireWindow):
        return Label(
            label=win.bind("title")
        )
    
    def search(self, query: str, search_size: int) -> list[Icon]:
        # itheme: Gtk.IconTheme = self._itheme
        # print(type(query))
        count = 0
        for item in self._list:
            if not query in item:
                continue
            # print(item)
            yield item
            count += 1
            if count >= search_size:
                break
        
        # while count < search_size:
        #     count += 1
        #     yield ""
        # return [ 'unknown', 'what' ]
    
    def build(self):
        search_size = 20
        items = list([Variable(value='') for i in range(0, search_size)])

        def setter(entry: Entry):
            res = list(self.search(entry.text, search_size))
            for i in range(0, search_size):
                if i >= len(res):
                    items[i].value = ''
                else:
                    items[i].value = res[i]
        
        entry = Entry(
            on_change=setter,
            width_request=300,
        )

        # def binding(x):
        #     s = list(self.search(x))
        #     print(f'SEARCH: {len(s)}')

        #     for item in s:
        #         yield self.item(item)
            # return map(self.item, s)
        size = 72

        return Box(
            vertical=True,
            child=[
                entry,
                Scroll(
                    height_request=500,
                    width_request=350,
                    child=Box(
                        vertical=True,
                        child=[
                            Box(
                                height_request=70,
                                # vertical=True,
                                child=[
                                    Icon(48, image=item.bind('value')),
                                    Label(label=item.bind('value')),
                                ]
                            ) for item in items
                        ],
                    )
                )
                
            ]
            # child=serv.bind('windows', lambda wins: [self.desc(w) for w in wins])
        )


Debug(0)


main()


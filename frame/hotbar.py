


import os.path as osp

from ignis.widgets import *
from ignis.variable import Variable

from gi.repository import Gtk # type: ignore

from ignis.services.applications import ApplicationsService, Application

from wm import Workspace, Frame


applications: ApplicationsService = ApplicationsService.get_default()
apps: list[Application] = applications.apps

# app executable -> app icon
icon_table: dict[str, str] = {}

def iconname(app: Application):
    classname = app.app.get_string("StartupWMClass")
    if classname != None:
        return classname
    return osp.basename(app.executable)

for app in apps:
    key = iconname(app)
    icon = app.icon
    if icon is None:
        icon = 'unknown'
    icon_table[key] = icon


ITEM_ACTIVE_CSS = "hotbar-item-active"
ITEM_GRABBED_CSS = "hotbar-item-grabbed"

class HotbarItem(EventBox):
    def __init__(self, frame: Frame):
        self._frame = frame

        # frame.workspace.connect("active_changed", )

        frame.connect("notify::active", self.activated)
        frame.connect("notify::grab", self.grabbed)
        # self._active_bind = frame.bind("active", self.active_changed)
        self._initialized = False
        super().__init__(
            css_classes=["hotbar-item"],
            child=self.build(),

            on_click=self.pressed
        )
        self._initialized = True

        if frame.active:
            self.add_css_class(ITEM_ACTIVE_CSS)
        if frame.grab:
            self.add_css_class(ITEM_GRABBED_CSS)

    def activated(self, frame: Frame, x):
        if self._initialized:
            if frame._active:
                self.add_css_class(ITEM_ACTIVE_CSS)
            else:
               self.remove_css_class(ITEM_ACTIVE_CSS)

    def grabbed(self, frame: Frame, x):
        if self._initialized:
            if frame._grab:
                self.add_css_class(ITEM_GRABBED_CSS)
                # print("Grab")
            else:
               self.remove_css_class(ITEM_GRABBED_CSS)
            #    print("Drop")

    def active_changed(self, workspace: Workspace, old: Frame, new: Frame):
        pass
        # print(f"Frame: {self._frame.window.title} .Active is {value}")
        # return value

    def pressed(self, x):
        # print("Pressed:", self._frame.window._title)
        self._frame.window.focus()

    def active_bind(self, active: bool):
        # print("Active:", active)
        if self._initialized:
            if active:
                self.add_css_class(ITEM_ACTIVE_CSS)
            else:
                self.remove_css_class(ITEM_ACTIVE_CSS)
            # print("Set Active:", active)
        return 'firefox' if active else 'unknown'
    
    def build(self):
        # print("Window APPID:", self._frame.window.app_id)
        iconname = icon_table.get(self._frame.window.app_id, 'unknown')
        return [
            Icon(
                pixel_size=48,
                image=iconname,
                tooltip_text=self._frame.window.bind('title'),
                # tooltip_text="TIP",
            )
        ]

class Hotbar(Window):
    __gtype_name__ = "HotbarWindow"
    def __init__(self, monitor: int, workspace: Workspace):
        self._workspace = workspace

        # self._ec = EventControllerKey()

        workspace.connect("active_changed", self.active_changed)
        workspace.connect("notify::active_frame", self.active_changed)
        workspace.connect("notify::shown", self.workspace_shown)

        super().__init__(
            css_classes=["hotbar"],
            anchor=[ "bottom" ],
            layer="overlay",
            exclusivity="ignore", # Whether to take up space
            margin_bottom=120,
            namespace=f"hotbar-window-{monitor}",
            kb_mode="exclusive", # 'exclusive' Will capture all Focus while Active
            popup=True,

            child=self.build(),
            title="Hotbar",
            # titlebar=HeaderBar(show_title_buttons=True),
        )

        self.connect("hide", self.hidden)

        # self.visible
        self.set_visible(False)
        key_controller = Gtk.EventControllerKey()
        self.add_controller(key_controller)
        key_controller.connect("key-released", self.key_released)

    def workspace_shown(self, workspace: Workspace, x):
        # print("Shown:", workspace.shown, " - ", workspace.active_frame)
        self.set_visible(workspace.shown)
        pass
        # self.chain = self.build()

    def hidden(self, x):
        if self._workspace.shown:
            self._workspace.shown_set(False)
        # print("Hidden", self._workspace.shown)

    def active_changed(self, workspace, old: Frame, new: Frame):
        oldname = "None"
        if old:
            oldname = old.window.title
        newname = "None"
        if new:
            newname = new.window.title

        # print(f"Active Changed: {oldname} -> {newname}")
        # self.set_visible(old is not None)

    def key_released(self, k, keyval: int, keycode: int, state):
        self._workspace.shown_set(False)
        # print("Key Released")
        # self.set_visible(False)

    # def active_changed(self, workspace, active):
    #     print("======")
    #     print("Active:", active)
    
    def build(self):
        # print("Build")
        return Box(
            child=self._workspace.bind('frames', lambda frames:
                [
                    HotbarItem(frame)
                    for idx, frame in enumerate(frames)
                ]
            )
        )






import os.path as osp

from ignis.widgets import *
from ignis.variable import Variable
from ignis.gobject import Binding

from gi.repository import Gtk, Graphene # type: ignore
from ignis.utils import monitor, Poll

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
            valign="end",
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
                css_classes=["hotbar-item-icon"],
                pixel_size=48,
                image=iconname,
                # tooltip_text=self._frame.window.bind('title'),
                tooltip_text=self._frame.bind('refcount', lambda rc: f'Refd: {rc}'),
                # tooltip_text="TIP",
            )
        ]

class TagGrid(RevealerWindow):
    __gtype_name__ = "FlameshellTagGrid"
    def __init__(self, monitor: int):

        self._items = list([self.item(num) for num in range(1, 10)])

        grid = Grid(
            column_num=3,
            row_num=3,
            child=self._items,
        )
        self.rev = Revealer(
            transition_type='crossfade',
            transition_duration=100,
            reveal_child=True,
            child=grid,
        )

        super().__init__(
            visible=False,
            revealer=self.rev,
            css_classes=["tag-grid-window"],
            anchor=[ "bottom", "left" ],
            margin_bottom=135,
            margin_left=500,
            namespace=f"hotbar-window-tag-grid-{monitor}",
            layer="overlay",
            child=Box(
                child=[self.rev]
            ),
        )

        # self.toggle()

    def track(self, item: HotbarItem, window: Window, container: Box) -> bool:
        ok, rect = item.compute_bounds(container)
        if not ok or window.monitor is None:
            print("Fail", ok, window.monitor)
            return False
        mon = monitor.get_monitor(window.monitor)
        if not mon:
            return False
        
        # Size of the Window
        ok, r_self = self.compute_bounds(self)
        self_width = r_self.get_width()

        if self_width < 10:
            return True # TRY AGAIN 15ms LATER

        monitor_width = mon.get_geometry().width # GDK Rectangle
        
        ok, r_con = container.compute_bounds(container)
        container_width = r_con.get_width()

        icon_x: int = rect.get_x() + (rect.get_width() / 2)
        
        # top_y
        margin = (monitor_width / 2)
        margin -= (container_width / 2)
        margin += icon_x

        margin -= (self_width / 2)
        
        self.margin_left = margin

        return False

    def item(self, num: int) -> any:
        size = 30
        return Button(
            vexpand=True, hexpand=True,
            width_request=size,
            height_request=size,
            css_classes=["tag-grid-button"],
            child=Label(label=f'{num}'),
        )

    def build(self):
        return Grid(
            css_classes=["tag-grid"],
            column_num=3,
            row_num=3,
            child=[self.item(num) for num in range(1, 10)],
        )

class Hotbar(Window):
    __gtype_name__ = "FlameshellHotbarWindow"
    def __init__(self, monitor: int, workspace: Workspace):
        self._workspace = workspace

        self._poll: Poll = Poll(2000, lambda x: 0)
        self._poll.cancel()
        self._poll_count: int = 0

        self._items = Variable(value=[])
        self._workspace.connect('notify::frames', self.__frames_changed)
        # self._items.connect("notify::value", self.item_binding)

        self._tg = TagGrid(monitor)

        self._items_container = Box(
            css_classes=["hotbar-box"],
            valign="end",
            halign="center",
            child=self._items.bind('value'),
        )

        workspace.connect("active_changed", self.active_changed)
        # workspace.connect("notify::active_frame", self.active_changed)
        workspace.connect("notify::shown", self.workspace_shown)

        def title_binding(frame: Frame) -> str:
            if frame is None:
                return ""
            return frame.window.title

        super().__init__(
            css_classes=["hotbar"],
            anchor=[ "bottom" ],
            layer="overlay",
            exclusivity="ignore", # Whether to take up space
            margin_bottom=75,
            namespace=f"hotbar-window-{monitor}",
            kb_mode="exclusive", # 'exclusive' Will capture all Focus while Active
            popup=True,
            monitor=monitor,

            child=Box(
                vertical=True,
                css_classes=[],
                child=[
                    self._items_container,
                    CenterBox(
                        center_widget= Label(
                            css_classes=["hotbar-title"],
                            halign="center",
                            label=self._workspace.bind('active_frame', title_binding),
                        ),
                    ),
                ]
            ),
            title="Hotbar",
        )

        self.connect("hide", self.hidden)

        # self.visible
        self.set_visible(False)
        key_controller = Gtk.EventControllerKey()
        self.add_controller(key_controller)
        key_controller.connect("key-released", self.key_released)

    def workspace_shown(self, workspace: Workspace, x):
        self.set_visible(workspace.shown)
        self._tg.visible = workspace.shown and workspace.active_frame is not None

    def hidden(self, x):
        if self._workspace.shown:
            self._workspace.shown_set(False)

    def active_changed(self, workspace, old: Frame, new: Frame):
        oldname = "None"
        if old:
            oldname = old.window.title
        newname = "None"
        if new:
            newname = new.window.title

            if self._poll:
                self._poll.cancel()
            
            self._poll_count = 0
            self._poll = Poll(15, self.track_callback)
            def cancel(x):
                self._poll_count += 1
                # Max 12 attempts
                if self._poll_count > 12 or self._poll.output == False:
                    self._poll.cancel()
            self._poll.connect('changed', cancel)

        
    def track_callback(self, poll: Poll) -> bool:
        try:
            it = self._items.value[self._workspace._active_idx]
            return self._tg.track(it, self, self._items_container)
        except:
            return False
        
    def key_released(self, k, keyval: int, keycode: int, state):
        self._workspace.shown_set(False)

    def __frames_changed(self, workspace: Workspace, x):
        self._items.value = list([
            HotbarItem(frame)
            for idx, frame in enumerate(workspace.frames)
        ])

    def item_binding(self, frames: list[Frame]) -> list[HotbarItem]:
        items: list[HotbarItem] = [
            HotbarItem(frame)
            for idx, frame in enumerate(frames)
        ]

        return items

    def build(self):
        def title_binding(frame: Frame) -> str:
            if frame is None:
                return ""
            
            return frame.window.title
        
        return Box(
            vertical=True,
            css_classes=[],
            child=[
                Box(
                    css_classes=["hotbar-box"],
                    valign="end",
                    halign="center",
                    child=self._items.bind('value'),
                ),
                CenterBox(
                    center_widget= Label(
                        css_classes=["hotbar-title"],
                        halign="center",
                        label=self._workspace.bind('active_frame', title_binding),
                    ),
                ),
            ]
        )



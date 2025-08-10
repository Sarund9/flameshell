


import os
import os.path as osp

from dataclasses import dataclass
from typing import Any, Protocol

from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty, DataGObject, IgnisSignal
from ignis import utils

from wayfire import WayfireSocket

from queue import Queue


WAYFIRE_SOCKET_DIR = ''

MATCH_DICT = {
    "class": "class_name",
    "initialClass": "initial_class",
    "initialTitle": "initial_title",
    "fullscreenClient": "fullscreen_client",
    "focusHistoryID": "focus_history_id",
    "inhibitingIdle": "inhibiting_idle",
}

@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

@dataclass
class Size:
    width: int
    height: int

class SocketAction(Protocol):
    def __call__(self, socket: WayfireSocket): ...

# class View:
#     activated: bool
#     app_id: str
#     base_geometry: Rect
#     bbox: Rect
#     focusable: bool
#     fullscreen: bool
#     geometry: Rect
#     id: int
#     last_focus_timestamp: int # UNIX TIME ? :: 3045295447114
#     layer: str # ENUM 'workspace'
#     mapped: bool # ???
#     max_size: Size
#     min_size: Size
#     minimized: bool
#     output_id: int
#     output_name: str
#     parent: int # -1
#     pid: int # -1
#     role: str # ENUM 'toplevel'
#     sticky: bool
#     tiled_edges: int # ???, was 0
#     title: str # zsh in svoid
#     type: str # ENUM 'toplevel
#     wset_index: int # Is this Workspace? 1




class WayfireWindow(DataGObject):
    # View Data:
    #     activated :: False
    #     app-id :: foot
    #     base-geometry :: {'height': 483, 'width': 693, 'x': 100, 'y': 100}
    #     bbox :: {'height': 483, 'width': 693, 'x': 100, 'y': 100}
    #     focusable :: True
    #     fullscreen :: False
    #     geometry :: {'height': 483, 'width': 693, 'x': 934, 'y': 428}
    #     id :: 134
    #     last-focus-timestamp :: 0
    #     layer :: workspace
    #     mapped :: True
    #     max-size :: {'height': 0, 'width': 0}
    #     min-size :: {'height': 23, 'width': 11}
    #     minimized :: False
    #     output-id :: 1
    #     output-name :: DP-1
    #     parent :: -1
    #     pid :: 15076
    #     role :: toplevel
    #     sticky :: False
    #     tiled-edges :: 0
    #     title :: foot
    #     type :: toplevel
    #     wset-index :: 1

    def __init__(self, service: 'WayfireService'):
        super().__init__(match_dict=MATCH_DICT)
        self._service = service
        self._activated: bool = False
        self._app_id: str = ""
        self._base_geometry: Rect = Rect(0, 0, 0, 0)
        self._bbox: Rect = Rect(0, 0, 0, 0)
        self._focusable: bool = False
        self._fullscreen: bool = False
        self._geometry: Rect = Rect(0, 0, 0, 0)
        self._id: str = ""
        self._last_focus_timestamp: int = 0 # TODO: Unix Time?
        self._layer: str = "" # ENUM 'workspace'
        self._mapped: bool = False
        self._max_size: Size = Size(0, 0)
        self._min_size: Size = Size(0, 0)
        self._minimized: bool = False
        self._output_id: int = -1
        self._output_name: str = ""
        self._parent: int = -1 # ???
        self._pid: int = 0
        self._role: str = ""
        self._sticky: bool = False
        self._tiled_edges: int = 0 # ???
        self._title: str = ""
        self._type: str = "" # ENUM 'toplevel'
        self._wset_index: int = 0

    @IgnisSignal
    def closed(self):
        """
        Emitted when the window has been closed.
        """

    def sync(self, view_data: dict[str, Any]) -> None:
        """
        :meta private:
        """
        data = {}
        for key, value in view_data.items():
            if '-' in key:
                data[key.replace('-', '_')] = value
            else:
                data[key] = value
        super().sync(data)

    def focus(self):
        def do(socket: WayfireSocket):
            socket.set_focus(self._id)
        self._service.dosocket(do)
        # self._service._socket.set_focus(self._id)

    @IgnisProperty
    def activated(self) -> bool:
        return self._activated
    
    @IgnisProperty
    def app_id(self) -> str:
        return self._app_id

    @IgnisProperty
    def base_geometry(self) -> Rect:
        return self._base_geometry

    @IgnisProperty
    def bbox(self) -> Rect:
        return self._bbox

    @IgnisProperty
    def focusable(self) -> bool:
        return self._focusable

    @IgnisProperty
    def fullscreen(self) -> bool:
        return self._fullscreen

    @IgnisProperty
    def geometry(self) -> Rect:
        return self._geometry

    @IgnisProperty
    def id(self) -> str:
        return self._id
    
    @IgnisProperty
    def last_focus_timestamp(self) -> int:
        return self._last_focus_timestamp
    
    @IgnisProperty
    def layer(self) -> str:
        return self._layer
    
    @IgnisProperty
    def mapped(self) -> bool:
        return self._mapped

    @IgnisProperty
    def max_size(self) -> Size:
        return self._max_size
    
    @IgnisProperty
    def min_size(self) -> Size:
        return self._min_size
    
    @IgnisProperty
    def minimized(self) -> bool:
        return self._minimized
    
    @IgnisProperty
    def output_id(self) -> int:
        return self._output_id
    
    @IgnisProperty
    def output_name(self) -> str:
        return self._output_name
    
    @IgnisProperty
    def parent(self) -> int:
        return self._parent
    
    @IgnisProperty
    def pid(self) -> int:
        return self._pid
    
    @IgnisProperty
    def role(self) -> str:
        return self._role
    
    @IgnisProperty
    def sticky(self) -> bool:
        return self._sticky
    
    @IgnisProperty
    def tiled_edges(self) -> int:
        return self._tiled_edges
    
    @IgnisProperty
    def title(self) -> str:
        return self._title
    
    @IgnisProperty
    def type(self) -> str:
        return self._type

    @IgnisProperty
    def wset_index(self) -> int:
        return self._wset_index


class WayfireService(BaseService):

    def __init__(self):
        super().__init__()


        self._debug = 0
        self._windows: dict[str, WayfireWindow] = {}
        self._focused_window: WayfireWindow = None

        self._bindings = {}

        self._socket = WayfireSocket()
        # self._socket.client.setblocking(False)
        self._cmd_socket = WayfireSocket()
        self._bind_queue = Queue()

        # if self.is_available:
        #     self.__listen_events()
        #     self.__initial_sync()

    @IgnisSignal
    def window_opened(self, window: WayfireWindow):
        """
        Emitted when a new window has been added.

        Args:
            window: The instance of the window.
        """

    def begin_listening(self):
        if self.is_available:
            self.__listen_events()
            self.__initial_sync()

    def dosocket(self, func: SocketAction):
        func(self._cmd_socket)

    @IgnisProperty
    def is_available(self) -> bool:
        """
        Whether Wayfire IPC is available.
        """
        sockname = os.getenv('WAYFIRE_SOCKET')
        return sockname is not None and osp.exists(sockname)

    @IgnisProperty
    def windows(self) -> list[WayfireWindow]:
        """
        A list of windows.
        """
        return list(self._windows.values())

    @IgnisProperty
    def focused_window(self) -> WayfireWindow:
        """
        The currently focused Window.
        """
        return self._focused_window

    # def trunc(self, data: str, max_len: int):
    #     return (data[:max_len] + '..') if len(data) > max_len else data

    def register_binding(self, binding: str, *, mode: str, exec_always: bool, callback: callable):
        # print("=====================================")
        # register_binding('KEY_LEFTSUPER', mode='press')
        # def register(socket: WayfireSocket):
        #     response = socket.register_binding(binding, mode=mode, exec_always=exec_always)
        #     # print("REGISTER BINDING:", response)
        #     if 'binding-id' not in response:
        #         return
        #     binding_id = response['binding-id']
        #     self._bindings[binding_id] = callback
        
        response = self._socket.register_binding(binding, mode=mode, exec_always=exec_always)
        # print("REGISTER BINDING:", response)
        if 'binding-id' not in response:
            return
        binding_id = response['binding-id']

        self._bindings[binding_id] = callback

    def __initial_sync(self):
        sock = self._cmd_socket

        views = sock.list_views(True) # Get toplevels
        for view in views:
            self.__window_opened(view)
        # self._windows = [WayfireWindow(view) for view in views]
        # for view in views:
        #     print("VIEW:", view)

    @utils.run_in_thread
    def __listen_events(self):
        self._socket.watch()

        while True:
            # if not self._bind_queue.empty():
            #     func = self._bind_queue.get()
            #     func(self._socket)

            msg = self._socket.read_next_event()
            if "event" in msg:
                self.__on_event_received(msg)

    def __on_event_received(self, msg: dict):
        """
        Other events:
            

        """
        event_type = msg.get("event")

        match event_type:
            case "command-binding":
                item = self._bindings.get(msg.get("binding-id"))
                if item is not None:
                    item()
                    # print("Received:", item)
                # print("Received Command Binding Event:", msg)
            case "view-mapped":
                self.__window_opened(msg.get("view"))
            case "view-unmapped":
                self.__window_closed(msg.get("view"))
            case "view-title-changed":
                self.__window_view_sync(msg.get("view"))
            case "view-focused":
                view = msg.get("view")
                if view is not None:
                    foc = self.__window_view_sync(view)
                    if foc is not None:
                        self._focused_window = foc
                        self.notify("focused_window")
            case "view-minimized":
                pass # TODO
            case "view-geometry-changed":
                self.__window_moved(msg.get("old-geometry"), msg.get("view"))
            case "view-set-output": # This was the First Message
                # output: None
                # view
                pass
            case "view-app-id-changed":    # ???
                pass
            case "view-workspace-changed": # Moved window to Workspace
                pass
            case "wset-workspace-changed": # Changed Workspace
                pass
            case "plugin-activation-state-changed":
                # plugin-activation-state-changed  - Plugin was Activated/Deactivated
                # output: int
                # output-data: {...}
                # plugin: str                      - Plugin was
                # state: bool                      - Activated/Deactivated
                pass
            case _:
                self._debug += 1
                print("")
                print(f"==== {self._debug} ====")
                print("Unhandled:", event_type)
                for key, value in msg.items():
                    print(f"  {key} :: {value}")

    def __window_opened(self, view: dict):
        if "type" not in view or view["type"] != "toplevel":
            return

        new_win = WayfireWindow(self)
        new_win.sync(view)

        self._windows[new_win.id] = new_win

        self.emit("window_opened", new_win)
        self.notify("windows")
        # print("View Mapped")

    def __window_closed(self, view: dict):
        id = view.get("id")
        if not id:
            return
        if id not in self._windows:
            return

        win = self._windows[id]
        win.emit("closed")

        del self._windows[id]
        self.notify("windows")
    
    # Syncronizes view data on a Window
    def __window_view_sync(self, view) -> WayfireWindow | None:
        id = view.get("id")
        if not id:
            return None
        if id not in self._windows:
            return None
        
        win = self._windows[id]
        win.sync(view)
        return win

    def __window_moved(self, old_geometry, view):
        win = self.__window_view_sync(view)
        if win is None:
            return

        # TODO: Trigger a moved IgnisSignal
        # Will take the old_geometry as Parameter
    
    def __plugin_activated(self, view):
        pass



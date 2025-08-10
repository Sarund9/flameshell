



from ignis.base_service import BaseService
from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal

import gi.repository as gir
import inspect

from utils import WayfireService, WayfireWindow


class Frame(DataGObject):
    def __init__(self, win: WayfireWindow, workspace: DataGObject):
        super().__init__()
        self.window = win
        self.workspace: 'Workspace' = workspace
        self._active: bool = False
        self._grab: bool = False

        workspace.connect("active_changed", self._active_changed)

        win.connect("closed", lambda win: self.emit("closed"))
        # self.active = workspace.bind('')
    
    @IgnisSignal
    def closed(self):
        pass

    def active_set(self, value: bool):
        self._active = value
        self.notify("active")
    
    @IgnisProperty(setter=active_set)
    def active(self) -> bool:
        return self._active


    def grab_set(self, value: bool):
        self._grab = value
        self.notify("grab")
    
    @IgnisProperty(setter=grab_set)
    def grab(self) -> bool:
        return self._grab

    def _active_changed(self, workspace, old, new):
        if old == self:
            self._active = False
            self.notify("active")
        if new == self:
            self._active = True
            self.notify("active")



class Workspace(DataGObject):
    def __init__(self):
        super().__init__()
        wayfire: WayfireService = WayfireService.get_default()

        self._frames: list[Frame] = []
        self._active_idx: int = -1
        self._shown: bool = False
        self._grab: bool = False
    
        wayfire.connect("window_opened", self.window_opened)
        wayfire.connect("notify::focused-window", self.window_focused)

    @IgnisSignal
    def active_changed(self, last: Frame, curr: Frame):
        """
        Emmited when the Active frame Changes
        """

    def window_opened(self, wayfire: WayfireService, window: WayfireWindow):
        def on_closed(frame: Frame):
            idx = self._frames.index(frame)
            frame = self._frames.pop(idx)

            self.notify("frames")

            if idx != self._active_idx:
                return

            new_idx = self._active_idx - 1
            if self._active_idx < 0 and len(self._frames) > 0:
                new_idx = 0
            
            frame.active_set(False) # Set active to False
            
            # Swap active Frame
            self._active_idx -= 1
            if self._active_idx < 0 and len(self._frames) > 0:
                self._active_idx = 0

            self.active_frame.active_set(True) # Set Active to True
        
            self.notify("active_frame")
            self.emit("active_changed", frame, self.active_frame)
        
        frame = Frame(window, self)
        self._frames.append(frame)
        frame.connect("closed", on_closed)

        self.notify("frames")

        if len(self._frames) == 1:
            self.__set_active(0)
            # self._active_idx = 0
            # self.notify("active_frame")

    def window_focused(self, wayfire: WayfireService, x):
        # focus = wayfire.focused_window
        # active: Frame = self.active_frame
        # if active.window.id == wayfire.foc
        # print("FOCUS")
        if not wayfire.focused_window:
            return
        
        idx = -1
        for i, frame in enumerate(self._frames):
            if not frame.window or not wayfire.focused_window:
                continue
            if frame.window.id == wayfire.focused_window.id:
                idx = i
                break
        
        if idx < 0:
            return
        
        # print("Focused:", idx)
        # self.__set_active(idx)

    def left(self):
        if len(self._frames) <= 1: # At least 2 frames are needed
            return
        if self._active_idx == 0:
            return # Already left-most
        
        if not self.shown:
            self.shown_set(True)
        self.__set_active(self._active_idx - 1)
        

    def right(self):
        if len(self._frames) <= 1: # At least 2 frames are needed
            return
        if self._active_idx == len(self._frames) - 1:
            return # Already right-most



        if not self.shown:
            self.shown_set(True)
        self.__set_active(self._active_idx + 1)

    def grab(self):
        frame = self.active_frame
        if not frame:
            return
        
        self._grab = not self._grab
        frame.grab_set(self._grab)

    @IgnisProperty
    def frames(self) -> list[Frame]:
        return self._frames
    
    @IgnisProperty
    def active_frame(self) -> Frame | None:
        if self._active_idx < 0:
            return None
        return self._frames[self._active_idx]

    def shown_set(self, value: bool):
        self._shown = value
        self.notify("shown")

    @IgnisProperty(setter=shown_set)
    def shown(self) -> bool:
        return self._shown

    def __set_active(self, idx: int):
        prev: Frame = None
        curr: Frame = None
        if self._active_idx > -1:
            self.active_frame.active_set(False)
            prev = self.active_frame
            # print("$$ Set False::", self.active_frame.window.title)
        self._active_idx = idx
        if self._active_idx > -1:
            self.active_frame.active_set(True)
            curr = self.active_frame
        
        # Focus the right window
        if curr:
            curr.window.focus()

        self.notify("active_frame")
        self.emit("active_changed", prev, curr)
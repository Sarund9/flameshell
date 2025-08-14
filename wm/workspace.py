



from ignis.base_service import BaseService
from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal

import gi.repository as gir
import inspect

from utils import WayfireService, WayfireWindow

from .frame import Frame
from .tags import Tag


class Workspace(DataGObject):
    def __init__(self):
        super().__init__()
        wayfire: WayfireService = WayfireService.get_default()

        self._frames: list[Frame] = []
        self._active_idx: int = -1
        self._shown: bool = False
        self._grab: bool = False
    
        # Create list of Tags 1-9
        self._tags: list[Tag] = list([Tag() for i in range(1, 10)])

        wayfire.connect("window_opened", self.__window_opened)
        wayfire.connect("notify::focused-window", self.__window_focused)

    @IgnisSignal
    def active_changed(self, last: Frame, curr: Frame):
        """
        Emmited when the Active frame Changes
        """

    @IgnisSignal
    def tag_changed(self, tag: Tag):
        """
        Emmited when a tag is changed
        """

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

    @IgnisProperty
    def tags(self) -> list[Tag]:
        return self._tags

    def left(self):
        if len(self._frames) <= 1: # At least 2 frames are needed
            return
        if self._active_idx == 0:
            return # Already left-most
        
        if not self.shown:
            self.shown_set(True)

        if self._grab:
            self.__swap_items(self._active_idx - 1)
        else:
            self.__set_active(self._active_idx - 1)
        

    def right(self):
        if len(self._frames) <= 1: # At least 2 frames are needed
            return
        if self._active_idx == len(self._frames) - 1:
            return # Already right-most

        if not self.shown:
            self.shown_set(True)

        if self._grab:
            self.__swap_items(self._active_idx + 1)
        else:
            self.__set_active(self._active_idx + 1)

    def grab(self):
        frame = self.active_frame
        if not frame:
            return
        
        self._grab = not self._grab
        frame.grab_set(self._grab)

    def toggle_tag(self, num: int):
        if num < 1 or num > 9:
            return
        # print("Toggle:", num)
        idx = num - 1
        tag = self._tags[idx]
        if not self._grab:
            if self.active_frame in tag:
                tag.remove(self.active_frame)
            else:
                tag.add(self.active_frame)
            self.__refresh_tag_focus()
            self.notify('tags')
            self.emit('tag_changed', tag)
            # print("Notify Tags")

    def __window_opened(self, wayfire: WayfireService, window: WayfireWindow):
        def on_closed(frame: Frame):
            idx = self._frames.index(frame)
            frame = self._frames.pop(idx)

            for tag in self._tags:
                tag.remove(frame)

            self.notify("frames")

            if idx != self._active_idx:
                return

            new_idx = self._active_idx - 1
            if self._active_idx < 0 and len(self._frames) > 0:
                new_idx = 0
            
            frame.active = False
            
            # Swap active Frame
            self._active_idx -= 1
            if self._active_idx < 0 and len(self._frames) > 0:
                self._active_idx = 0

            self.active_frame.active = True # Set Active to True
        
            self.notify("active_frame")
            self.emit("active_changed", frame, self.active_frame)
            self.__refresh_tag_focus()
        
        frame = Frame(window, self)
        self._frames.append(frame)
        frame.connect("closed", on_closed)

        self._tags[0].add(frame)

        self.notify("frames")

        if len(self._frames) == 1:
            self.__set_active(0)
            # self._active_idx = 0
            self.notify("active_frame")
            self.__refresh_tag_focus()

    def __window_focused(self, wayfire: WayfireService, x):
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

    def __swap_items(self, idx: int):
        active = self.active_frame
        swap   = self._frames[idx]

        self._frames[idx]               = active
        self._frames[self._active_idx]  = swap

        self._active_idx = idx

        self.notify('frames')

        # fa = self._frames[a]
        # fb = self._frames[b]
        
        # self._frames[a] = fa
        # self._frames[b] = fb

    def __set_active(self, idx: int):
        prev: Frame = None
        curr: Frame = None
        if self._active_idx > -1:
            self.active_frame.active = False
            prev = self.active_frame
            # print("$$ Set False::", self.active_frame.window.title)
        self._active_idx = idx
        if self._active_idx > -1:
            self.active_frame.active = True
            curr = self.active_frame
        
        # Focus the right window
        if curr:
            curr.window.focus()

        self.notify("active_frame")
        self.emit("active_changed", prev, curr)
        self.__refresh_tag_focus()

    def __refresh_tag_focus(self):
        # print("Refresh Tag Focus")
        for tag in self._tags:
            tag.focused = self.active_frame in tag

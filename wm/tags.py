


from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal

from .frame import Frame


class Tag(DataGObject):
    def __init__(self):
        super().__init__()

        self._enabled: bool = False
        self._focused: bool = False
        self._frames: set[Frame] = set()
    
    @IgnisProperty
    def enabled(self) -> bool:
        return self._enabled
    
    @enabled.setter
    def set_enabled(self, value: bool):
        if self._enabled == value:
            return

        self._enabled = value
        if value:
            for frame in self._frames:
                frame.tag_ref()
        else:
            for frame in self._frames:
                frame.tag_unref()

    @IgnisProperty
    def focused(self) -> bool:
        return self._focused
    
    @focused.setter
    def set_focused(self, value: bool):
        if self._focused == value:
            return
        
        self._focused = value
        if value:
            for frame in self._frames:
                frame.tag_ref()
        else:
            for frame in self._frames:
                frame.tag_unref()


    def add(self, frame: Frame) -> bool:
        if frame in self._frames:
            return False
        
        self._frames.add(frame)
        if self._enabled:
            frame.tag_ref()
        if self._focused:
            frame.tag_ref()
        return True

    def remove(self, frame: Frame) -> bool:
        if frame not in self._frames:
            return False
        self._frames.remove(frame)
        if self._enabled:
            frame.tag_unref()
        if self._focused:
            frame.tag_unref()
        return True

    def __contains__(self, frame: Frame) -> bool:
        return frame in self._frames
    


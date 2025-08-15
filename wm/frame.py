

from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal

from utils import WayfireService, WayfireWindow




class Frame(DataGObject):
    def __init__(self, win: WayfireWindow, workspace: DataGObject):
        super().__init__()
        self.window = win
        self.workspace: 'Workspace' = workspace
        self._active: bool = False
        self._grab: bool = False
        self._refcount: int = 0

        workspace.connect("active_changed", self._active_changed)

        win.connect("closed", lambda win: self.emit("closed"))

        self.window.minimized = True

        # self.active = workspace.bind('')
    
    @IgnisSignal
    def closed(self):
        pass

    @IgnisProperty
    def active(self) -> bool:
        return self._active

    @active.setter
    def set_active(self, value: bool):
        self._active = value
        self.notify("active")
        
        # if value:
        #     self.tag_ref()
        # else:
        #     self.tag_unref()
        # if value:
        #     if self._refcount < 1:
        #         self.window.minimized = False
        # else:
        #     if self._refcount < 1:
        #         self.window.minimized = False
    
    def grab_set(self, value: bool):
        self._grab = value
        self.notify("grab")
    
    @IgnisProperty
    def refcount(self) -> int:
        return self._refcount

    @IgnisProperty(setter=grab_set)
    def grab(self) -> bool:
        return self._grab

    def tag_ref(self):
        self._refcount += 1
        self.notify('refcount')
        if self._refcount == 1: # increased from 0 to 1
            self.window.minimized = False
    
    def tag_unref(self):
        self._refcount -= 1
        self.notify('refcount')
        if self._refcount == 0: # decreased from 1 to 0
            self.window.minimized = True

    def _active_changed(self, workspace, old, new):
        if old == self:
            self._active = False
            self.notify("active")
        if new == self:
            self._active = True
            self.notify("active")

    # def __update_visible(self):
    #     if self.window.minimized:
    #         if self.active:
    #             self.window.minimized = False
    #         elif self._refcount > 0:
    #             self.window.minimized = False
    #     else:
    #         if self._refcount < 1 and not self.active:
    #             self.window.minimized = True

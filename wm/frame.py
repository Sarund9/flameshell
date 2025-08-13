

from ignis.gobject import DataGObject, IgnisProperty, IgnisSignal

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

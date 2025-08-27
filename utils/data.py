

import os
import os.path as osp
import json


def get_path() -> str:
    def share() -> str:
        xdg = os.getenv('XDG_DATA_HOME')
        if xdg:
            print('XDG')
            return xdg
        home = os.getenv('HOME')
        if not home:
            raise Exception('HOME envar not Set.')
        return osp.join(home, '.local/share')

    sdir = share()

    path = osp.join(sdir, 'flameshell')

    return path

def is_serializable(obj: any) -> bool:
    return (
        hasattr(obj, 'load') and
        hasattr(obj, 'save') and
        callable(getattr(obj, 'load')) and
        callable(getattr(obj, 'save'))
    )




class Data:
    def __init__(self):
        self.data: dict = {}
        self.stack: list = []

    def load(self) -> bool:
        path = get_path()
        if not osp.isdir(path):
            return False # No data
        datapath = osp.join(path, 'data.json')
        if not osp.isfile(datapath):
            return False

        with open(datapath, 'r') as file:
            self.data = json.load(file)
        
        return True

    def save(self):
        path = get_path()
        if not osp.isdir(path):
            os.makedirs(path)
        
        datapath = osp.join(path, 'data.json')

        json_str = json.dumps(self.data, indent=4)

        with open(datapath, 'w') as file:
            file.write(json_str)

    def current(self) -> dict:
        if len(self.stack) == 0:
            return self.data
        return self.stack[len(self.stack) - 1]

    def begin(self, key: str):
        curr = self.current()
        if key not in curr:
            new = {}
            curr[key] = new # Set to dict
            self.stack.append(new)
            # print('key', key, 'not found')
        elif isinstance(curr[key], list):
            # If list, append to it.
            new = {}
            curr[key].append(new)
            self.stack.append(new)
        elif not isinstance(curr[key], dict):
            new = {}
            curr[key] = new # Set to dict
            self.stack.append(new)
            # print('Key', key, 'not a Dict:', type(curr[key]))
        else:
            # print('Descend into', key)
            self.stack.append(curr[key])

    def end(self):
        if len(self.stack) == 0:
            return
        self.stack.pop()

    def clear(self):
        curr = self.current()
        curr.clear()

    def array(self, key: str):
        curr = self.current()
        if key not in curr or not isinstance(curr[key], list):
            curr[key] = []


    def setval(self, key: str, value: any):
        curr = self.current()
        curr[key] = value

    def getval(self, key: str, default=None) -> any:
        curr = self.current()
        return curr.get(key, default)

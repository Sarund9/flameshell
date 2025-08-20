


import datetime

from ignis import utils
import ignis
from ignis.widgets import Widget
from ignis.utils import Utils

# from .pad import StatusPad



# class StatusClock(StatusPad):
#     def __init__(self, monitor: int):

#         super().__init__(
#             "clock", monitor,
#             menu=Calendar(),
#             child=[Clock("%H:%M", "%d %B")],
#         )

# class Clock(Widget.Box):
#     time: Widget.Label
#     date: Widget.Label

#     def __init__(self, time_fmt: str, date_fmt: str):
#         self.time_fmt = time_fmt
#         self.time = Widget.Label(
#             css_classes=["time"],
#             label = ""
#         )

#         self.date_fmt = date_fmt
#         self.date = Widget.Label(
#             css_classes=["date"],
#             label = ""
#         )

#         Utils.Poll(
#             1_000, self.update
#         )
        
#         super().__init__(
#             css_classes=["clock", ""],
#             vertical=True,
#             spacing=0,
#             child=[self.time, self.date]
#         )

#     def update(self, a):
#         now = datetime.datetime.now()
#         self.time.set_label(now.strftime(self.time_fmt))
#         self.date.set_label(now.strftime(self.date_fmt))

# class Calendar(Widget.Box):
    
#     def __init__(self):
#         now = datetime.datetime.now()

#         super().__init__(
#             css_classes=["status-calendar"],
#             vertical=True,
#             child=[
#                 Widget.CenterBox(
#                     start_widget=Clock("%H:%M:%S", "%d %b %Y"),
#                 ),
#                 Widget.Calendar(
#                     day=now.day,
#                     month=now.month - 1,
#                     year=now.year,
#                 )
#             ]
#         )




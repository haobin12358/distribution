# *- coding:utf8 *-
from control.COrder import COrder
import threading
print "start timer_fun after 100s!"
timer = threading.Timer(5, COrder().timer_fun)  # 首次启动定时器
timer.start()
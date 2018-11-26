# *- coding:utf8 *-
from control.COrder import COrder
from control.CAccount import CAccount
import threading

print "start timer_fun after 100s!"
timer = threading.Timer(100, COrder().timer_fun)  # 首次启动定时器
timer.start()

print "start deal_profit_fail after 5s!"
timer = threading.Timer(5, CAccount().deal_reward_discount)  # 首次启动处理奖金定时器
timer.start()
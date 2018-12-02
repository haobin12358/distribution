# *- coding:utf8 *-
from control.COrder import COrder
from control.CAccount import CAccount
import threading

print "start timer_fun after 5s!"
timer1 = threading.Timer(5, COrder().timer_fun)  # 首次启动定时器
timer1.setDaemon(True)
timer1.start()

print "start deal_profit_fail after 5s!"
timer2 = threading.Timer(5, CAccount().deal_reward_discount)  # 首次启动处理奖金定时器
timer2.setDaemon(True)
timer2.start()
# -*- coding:utf8 -*-
from configparser import ConfigParser

def modify(alipaynum, alipayname, bankname, accountname, cardnum, money, service, drawbank, bail, reward, sendname
           , sendphone, sendaddress):
    fp = 'config/setting.ini'  # 定义配置文件名
    conf = ConfigParser()  # 实例化
    conf.read(fp)  # 打开conf
    option = conf.options('account')
    print(option)
    item = conf.items('account')
    print(item)
    conf.set('account', 'alipaynum', alipaynum)
    conf.set('account', 'alipayname', alipayname)
    conf.set('account', 'bankname', bankname)
    conf.set('account', 'accountname', accountname)
    conf.set('account', 'cardnum', cardnum)
    conf.set('account', 'money', money)
    conf.set('account', 'service', service)
    conf.set('account', 'drawbank', drawbank)
    conf.set('account', 'bail', bail)
    conf.set('account', 'reward', reward)
    conf.set('account', 'sendname', sendname)
    conf.set('account', 'sendphone', sendphone)
    conf.set('account', 'sendaddress', sendaddress)
    with open("config/setting.ini", "w+") as f:
        conf.write(f)
    return True
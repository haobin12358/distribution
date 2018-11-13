# -*- coding:utf8 -*-
import os
import platform
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime, date, timedelta
from config.setting import QRCODEHOSTNAME
from common.timeformat import format_for_db, get_random_str, format_for_db_no_HMS, get_random_int\
    , format_forweb_no_HMS, format_for_dbmonth, get_random_str

def make_pic(name, wechat, idcardnum):
    starttime = datetime.strftime(datetime.now(), format_forweb_no_HMS)
    endtime = str(int(starttime[0:4]) + 2) + starttime[4:]
    id = get_random_str(12)
    im = Image.open("/opt/beili/file/shouquan.png")  # 打开文件
    # im = Image.open("/Users/fx/Desktop/shouquan.png")  # 打开文件
    print(im.format, im.size, im.mode)
    draw = ImageDraw.Draw(im)  # 修改图片
    ttfont = ImageFont.truetype("/home/www/楷体GB2312.ttf", 50)
    draw.text((630, 985), name.encode("utf-8"), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1075), wechat, fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1170), idcardnum, fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1270), unicode(id, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    ttfont = ImageFont.truetype("/home/www/楷体GB2312.ttf", 40)
    draw.text((900, 1760), unicode(starttime, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((1160, 1760), unicode(endtime, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    if platform.system() == "Windows":
        rootdir = "D:/task"
    else:
        rootdir = "/opt/beili/file/"
    if not os.path.isdir(rootdir):
        os.makedirs(rootdir)
    filepath = os.path.join(rootdir, id + '.png')
    im.save(filepath)
    # url = QRCODEHOSTNAME + "/file/" + id + '.png'
    url = QRCODEHOSTNAME + "/file/" + id + '.png'
    return url

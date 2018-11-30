# -*- coding:utf8 -*-
import os
import platform
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime, date, timedelta
from config.setting import QRCODEHOSTNAME
from common.timeformat import format_for_db, get_random_str, format_for_db_no_HMS, get_random_int\
    , format_forweb_no_HMS, format_for_dbmonth, get_random_str

def make_pic(name, wechat, id, idcardnum):
    starttime = datetime.strftime(datetime.now(), format_forweb_no_HMS)
    endtime = str(int(starttime[0:4]) + 2) + starttime[4:]
    idcardnum = idcardnum[:8] + '******' + idcardnum[14:]
    im = Image.open("/opt/beili/file/shouquan.png")  # 打开文件
    # im = Image.open("/Users/fx/Desktop/shouquan.png")  # 打开文件
    print(im.format, im.size, im.mode)
    draw = ImageDraw.Draw(im)  # 修改图片
    ttfont = ImageFont.truetype("/home/www/楷体GB2312.ttf", 50)
    draw.text((630, 985), name, fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1075), wechat, fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1170), idcardnum, fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1270), id, fill=(0, 0, 0), font=ttfont, anchor=2)
    ttfont = ImageFont.truetype("/home/www/楷体GB2312.ttf", 40)
    draw.text((900, 1760), starttime, fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((1160, 1760), endtime, fill=(0, 0, 0), font=ttfont, anchor=2)
    if platform.system() == "Windows":
        rootdir = "D:/task"
    else:
        rootdir = "/opt/beili/file/"
    if not os.path.isdir(rootdir):
        os.makedirs(rootdir)
    w, h = im.size
    filepath = os.path.join(rootdir, id + '.png')
    im.save(filepath, 'png', quality=90)
    # url = QRCODEHOSTNAME + "/file/" + id + '.png'
    url = QRCODEHOSTNAME + "/file/" + id + '.png'
    return url

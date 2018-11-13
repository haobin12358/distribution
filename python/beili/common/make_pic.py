# -*- coding:utf8 -*-

from PIL import Image, ImageFont, ImageDraw
from datetime import datetime, date, timedelta
from common.timeformat import format_for_db, get_random_str, format_for_db_no_HMS, get_random_int\
    , format_forweb_no_HMS, format_for_dbmonth, get_random_str

def make_pic(name, wechat, idcardnum):
    starttime = datetime.strftime(datetime.now(), format_forweb_no_HMS)
    endtime = str(int(starttime[0:4]) + 2) + starttime[4:]
    id = get_random_str(12)
    im = Image.open("/Users/fx/Desktop/WechatIMG4043.png")  # 打开文件
    print(im.format, im.size, im.mode)
    draw = ImageDraw.Draw(im)  # 修改图片
    ttfont = ImageFont.truetype("/Users/fx/Downloads/楷体GB2312.ttf", 50)
    draw.text((630, 985), unicode(name,'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1075), unicode(wechat, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1170), unicode(idcardnum, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1270), unicode(id, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    ttfont = ImageFont.truetype("/Users/fx/Downloads/楷体GB2312.ttf", 40)
    draw.text((900, 1760), unicode(starttime, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=1)
    draw.text((1160, 1760), unicode(endtime, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    im.show()

if __name__ == '__main__':
    make_pic('冯欣', 'youknowfx', '511332425345345011')
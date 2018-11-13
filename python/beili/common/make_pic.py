# -*- coding:utf8 -*-

from PIL import Image, ImageFont, ImageDraw

def make_pic(name, wechat, idcardnum, id):
    im = Image.open("/Users/fx/Desktop/WechatIMG4043.png")  # 打开文件
    print(im.format, im.size, im.mode)
    draw = ImageDraw.Draw(im)  # 修改图片
    ttfont = ImageFont.truetype("/Users/fx/Downloads/楷体GB2312.ttf", 50)
    draw.text((630, 985), unicode(name,'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1075), unicode(wechat, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1170), unicode(idcardnum, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    draw.text((720, 1270), unicode(id, 'utf-8'), fill=(0, 0, 0), font=ttfont, anchor=2)
    im.show()

if __name__ == '__main__':
    make_pic('冯欣', 'youknowfx', '511332425345345011', 'dwefquiq')
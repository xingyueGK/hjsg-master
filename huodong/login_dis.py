#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 16:35
# @Author  : xingyue
# @File    : login_dis.py

import requests
import os
import pytesseract
from PIL import Image
from collections import defaultdict

session=requests.session()

#获取登录窗口中的loginhash和formhash
def get_login_window():
    url='http://bbs.hjsg.zhanchengkeji.com/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    headers={'Host':'bbs.hjsg.zhanchengkeji.com','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','X-Requested-With':'XMLHttpRequest','Accept':'*/*','Referer':'http://www.discuz.net/forum.php','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8'}
    #清空原来的headers
    session.headers.clear()
    #更新headers
    session.headers.update(headers)
    r=session.get(url)
    #获取loginhash
    p=r.text.find('loginhash')+len('loginhash')+1
    loginhash=r.text[p:p+5]
    #获取formhash
    p=r.text.find('formhash')+len('formhash" value="')
    formhash=r.text[p:p+8]
    return (loginhash,formhash)

#获取update
def get_code_info():
    url='http://bbs.hjsg.zhanchengkeji.com/misc.php?mod=seccode&action=update&idhash=cSA&0.3916181418197131&modid=member::logging'
    r=session.get(url)
    p=r.text.find('update=')
    update=r.text[p+7:p+12]
    return update

#获取验证码
def get_code(update):
    url='http://bbs.hjsg.zhanchengkeji.com/misc.php?mod=seccode&update='+update+'&idhash=cSA'
    headers={'Host':'bbs.hjsg.zhanchengkeji.com','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Accept':'image/webp,image/*,*/*;q=0.8','Referer':'http://www.discuz.net/forum.php','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8'}
    session.headers.clear()
    session.headers.update(headers)
    r=session.get(url)
    print r.content[:3]
    # if(r.content[:3]==b'PNG'):
    #     #保存验证码图片
    file=open('code.gif','wb')
    file.write(r.content)
    file.close()
    # else:
    #     #打印错误信息
    #     print(r.text)

#检查验证码是否正确
#通过人工识别验证码code，:)
def check_code(code):
    url='http://bbs.hjsg.zhanchengkeji.com/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash=cSA&secverify='+code
    headers={'Host':'bbs.hjsg.zhanchengkeji.com','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Accept':'image/webp,image/*,*/*;q=0.8','Referer':'http://www.discuz.net/forum.php','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8'}
    session.headers.clear()
    session.headers.update(headers)
    r=session.get(url)
    return r.text

#模拟登录
def login(loginhash,formhash,code,username,password):
    url='http://bbs.hjsg.zhanchengkeji.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash='+loginhash+'&inajax=1'
    data={'formhash':formhash,
          'referer':'http://bbs.hjsg.zhanyougame.com',
          'loginfield':'username',
          'username':username,
          'password':password,
          'questionid':'0',
          'answer':'',
          'sechash':'SAsg8XJ20',
          # 'seccodemodid':'member::logging',
          'seccodeverify':code}
    headers={'Host':'bbs.hjsg.zhanchengkeji.com','Connection':'keep-alive','Content-Length':'203','Cache-Control':'max-age=0','Origin':'http://bbs.hjsg.zhanchengkeji.com','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer':'http://bbs.hjsg.zhanchengkeji.com/forum.php','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.8'}
    session.headers.clear()
    session.headers.update(headers)
    r=session.post(url,data)
    print(r.text)


# (loginhash,formhash)=get_login_window()
# get_code(get_code_info())
# code=raw_input()#人工识别 :)
# check_code(code)
# #[CDATA[succeed]]
# login(loginhash,formhash,code,123,'afd')
#欢迎您回来，现在将转入登录前页面



# tesseract.exe所在的文件路径
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files (x86)\Tesseract-OCR\\tesseract'



# 获取图片中像素点数量最多的像素
def get_threshold(image):
    pixel_dict = defaultdict(int)

    # 像素及该像素出现次数的字典
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1

    count_max = max(pixel_dict.values())  # 获取像素出现出多的次数
    pixel_dict_reverse = {v: k for k, v in pixel_dict.items()}
    threshold = pixel_dict_reverse[count_max]  # 获取出现次数最多的像素点

    return threshold


# 按照阈值进行二值化处理
# threshold: 像素阈值
def get_bin_table(threshold):
    # 获取灰度转二值的映射table
    table = []
    for i in range(256):
        rate = 0.1  # 在threshold的适当范围内进行处理
        if threshold * (1 - rate) <= i <= threshold * (1 + rate):
            table.append(1)
        else:
            table.append(0)
    return table


# 去掉二值化处理后的图片中的噪声点
def cut_noise(image):
    rows, cols = image.size  # 图片的宽度和高度
    change_pos = []  # 记录噪声点位置

    # 遍历图片中的每个点，除掉边缘
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # pixel_set用来记录该店附近的黑色像素的数量
            pixel_set = []
            # 取该点的邻域为以该点为中心的九宫格
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if image.getpixel((m, n)) != 1:  # 1为白色,0位黑色
                        pixel_set.append(image.getpixel((m, n)))

            # 如果该位置的九宫内的黑色数量小于等于4，则判断为噪声
            if len(pixel_set) <= 4:
                change_pos.append((i, j))

    # 对相应位置进行像素修改，将噪声处的像素置为1（白色）
    for pos in change_pos:
        image.putpixel(pos, 1)

    return image  # 返回修改后的图片


# 识别图片中的数字加字母
# 传入参数为图片路径，返回结果为：识别结果
def OCR_lmj(img_path):
    image = Image.open(img_path)  # 打开图片文件
    imgry = image.convert('L')  # 转化为灰度图

    # 获取图片中的出现次数最多的像素，即为该图片的背景
    max_pixel = get_threshold(imgry)
    # 将图片进行二值化处理
    table = get_bin_table(threshold=max_pixel)
    out = imgry.point(table, '1')
    # 去掉图片中的噪声（孤立点）
    out = cut_noise(out)

    #保存图片
    out.save('D:\hjsg\huodong\img_gray.jpg')

    # 仅识别图片中的数字
    # text = pytesseract.image_to_string(out, config='digits')
    # 识别图片中的数字和字母
    text = pytesseract.image_to_string(image)
    print text
    # 去掉识别结果中的特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])
    # print(text)

    return text


def main():
    # 识别指定文件目录下的图片
    # 图片存放目录figures
    dir = 'D:\hjsg\huodong'

    correct_count = 0  # 图片总数
    total_count = 0  # 识别正确的图片数量

    # 遍历figures下的png,jpg文件
    for file in os.listdir(dir):
        if file.endswith('.png') or file.endswith('.gif'):
            # print(file)
            image_path = '%s/%s' % (dir, file)  # 图片路径

            answer = file.split('.')[0]  # 图片名称，即图片中的正确文字
            recognizition = OCR_lmj(image_path)  # 图片识别的文字结果
            print answer, recognizition
            if recognizition == answer:  # 如果识别结果正确，则total_count加1
                correct_count += 1
            total_count += 1

    print('Total count: %d, correct: %d.' % (total_count, correct_count))
    '''
    # 单张图片识别
    image_path = 'E://figures/code (1).jpg'
    OCR_lmj(image_path)
    '''


main()
'''
File Name: AllPics
Description: 
Author: jwj
Date: 2018/1/20
'''
__author__ = 'jwj'

import requests
from bs4 import BeautifulSoup
from AModel import AModel

def get_html(url, k=3):
    count = 0
    while count < k:
        html = requests.get(url)
        if html:
            return html.text
        count += 1
    return None


def get_info(html):
    html_soup = BeautifulSoup(html, 'html.parser')
    select_list = html_soup.select(".lb_box dl dd a")
    if select_list:
        for item in select_list:
            url = item['href']   # 跳转链接
            title = item.string  # 该组图片的标题
            model = AModel(url, title)
            model.get_img_urls()   # 获取该组图片的所有链接
            model.save_to_dir()    # 保存图片到文件夹下


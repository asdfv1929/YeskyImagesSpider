'''
File Name: AModel
Description: 基本单元模型，存储某一组的基本信息、图片链接等，可进行下载图片
Author: jwj
Date: 2018/1/20
'''
__author__ = 'jwj'

import requests
from bs4 import BeautifulSoup
import urllib
import os
import threading


class AModel(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.img_urls_list = []   # 列表，存储图片的链接

    # 获取网页源码，带容错
    def get_html(self, url, k=3):
        count = 0
        while count < k:
            html = requests.get(url)
            if html:
                return html.text
            count += 1
        return None

    def get_html_soup(self, url):
        html = self.get_html(url)
        if not html:
            print("It does not get the html.")
            return None
        html_soup = BeautifulSoup(html, 'html.parser')
        return html_soup

    # 返回该页面上的图片链接
    def get_img(self, url):
        html_soup = self.get_html_soup(url)
        if not html_soup:
            return None
        select_list = html_soup.select(".l_effect_img_mid a img")
        if not select_list:
            print("select mistake.")
            return None
        item = select_list[0]
        return item['src']

    # 保存所有图片的链接到列表（嵌套列表）
    def get_img_urls(self):
        html_soup = self.get_html_soup(self.url)
        img_set = []
        select_list = html_soup.select(".overview ul li a")
        if select_list:
            for item in select_list:
                img_url = self.get_img(item['href'])
                img_set.append(img_url)
        self.img_urls_list.append(img_set)

    # 获取图片的名称，如 77VQ96UV4D9F.jpg
    def get_img_name(self, url):
        return url.split('/')[-1]

    # 消除一些影响创建文件夹的特殊字符
    def del_special_symbol(self, string):
        return string.replace(':', '').replace('"', '').replace('?', '').strip()

    # 保存图片至本地
    def download_img(self, urls_list, file_path):
        for url in urls_list:   # 遍历一组照片链接列表
            urllib.request.urlretrieve(url, file_path + '\\' + self.get_img_name(url))  # 下载图片

    # 创建文件夹，并保存图片
    def save_to_dir(self):
        for item in self.img_urls_list:  # 遍历各组图片链接列表
            print(self.title, ' downloading...')
            file_path = 'yeskyImgs\%s' % self.del_special_symbol(self.title)  # 路径
            if not os.path.exists(file_path):
                os.makedirs(file_path)  # 创建该组图片的文件夹
            th = threading.Thread(target=self.download_img(item, file_path))  # 下载该组图片
            th.start()

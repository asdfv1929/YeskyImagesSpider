'''
File Name: main
Description: 
Author: jwj
Date: 2018/1/20
'''
__author__ = 'jwj'

import time
import AllPics

if __name__ == '__main__':
    url = 'http://pic.yesky.com/c/6_20491_%s.shtml'
    start = time.time()
    for page in range(1, 2):
        html = AllPics.get_html(url % page)
        AllPics.get_info(html)
    end = time.time()
    print('%.2f seconds' % (end - start))

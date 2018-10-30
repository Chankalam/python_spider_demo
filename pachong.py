#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time;
import json;
import requests;
import os;
import sys;
import urllib;
import random;
from urllib import request;
from bs4 import BeautifulSoup


class TmallSpider:
    UA = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
          "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"]
    headers = {
        "Accept": "application/json,text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "CheckError": "check",
        "Cookie": "TYCID=79ecda1ebc7243bb8e0e61001fa62e45; tnet=219.217.246.3; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1478185016,1478185105; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1478185127; RTYCID=f6052f4746504a92a9449adf8c1aad4d; aliyungf_tc=AQAAAIi4rlRU9QIAA/bZ26bXAnGDUsL8; _pk_id.1.4c4c=ff85a162bc61332e.1478185118.1.1478185128.1478185118.; _pk_ref.1.4c4c=%5B%22%22%2C%22%22%2C1478185118%2C%22http%3A%2F%2Fwww.tianyancha.com%2F%22%5D; _pk_ses.1.4c4c=*; token=70f49be8c16c4cb290fa7d05c8a60638; _utm=-24s2tr4st24-9n8d32849t38sk97hh8",
        "Referer": "http://bj.tianyancha.com/search",
        "Tyc-From": "normal",
        "User-Agent": random.choice(UA),
        "loop": "null"
    }

    def __init__(self):
        print('--欢迎使用商品晒图抓取工具--')

    def crawl(self, item_id, max_page='0', save_root='d:/python_spider'):
        max_page = int(max_page)
        pic_count = 1  # 下载量计数
        page = 1  # 当前页
        has_next = True
        save_root = save_root + '/' + item_id
        pathIsExists = os.path.exists(save_root)
        if not pathIsExists:
            os.makedirs(save_root)
            print('已创建图片存储文件夹：' + save_root)

        while has_next:

            api_url = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + item_id + "&\
spuId=988489071&sellerId=3919498123&order=3&\
currentPage=" + str(page) + "&append=0&content=1&tagId=&posi=&picture=1&groupId=&\
a=098%23E1hvIQvcvcWvjQCkvvvvvjiPR2s90j18R2z96j1VPmPUsjEHn2cUsjnvRsLW1jWtvpvhvvvvvUhCvvsNq%2Faw3HdNz1vkRYArvpvEvCpK9KMS2h%2FMdphvmpvUsg8kI9QmnQwCvvNNzYsw7lOkCQhvCYMNzn1fx7JrvpvbmCkXvEAwCbWvIL8rvpvBUCC8vxX7v81C84%2F9bZbxKaVjvpvhvvpvv8wCvvpvvUmm2QhvCPMMvvvCvpvVvvpvvhCvuphvmvvv92RmchcFkphvC99vvOC0BfyCvm9vvvvvphvvvvvvv61vpCpQvvvHvhCvHUUvvvZvphvZm9vvCpCvpCp8mphvLvBaavvjw%2Bet9E7re169D7zZaB4AVAtlYExreTt%2Bm7zwaNoAdcZI%2BExr18TJEcqwafmD5i10Bq2XS4ZAhjvnY42B%2BbJcwyf1Q8L%2BWLytvpvhvvvvv86CvCUyHCv2hCvhDzTnrsXrmRjBAO7CvpvWz%2FYIPva4zYM5jYdwRphvCvvvvvvtvpvhvvvvv2yCvvpvvvvvdphvmpvUxvHAw3QE6Q%3D%3D&\
itemPropertyId=&itemPropertyIndex=&userPropertyId=&userPropertyIndex=&rateQuery=&location=&needFold=0&_ksTS=1540868119686_1538&callback=replacestr"
            #print(api_url)

            req = requests.get(api_url)
            json_str = req.text.replace('replacestr(', '')
            json_str = json_str[:-1]

            datas = json.loads(json_str, encoding='utf-8')
            datas = datas['rateDetail']['rateList']
            # print(datas)

            if len(datas) > 0 and page <= max_page:
                for x in datas:
                    pic_urls = x['pics']
                    for pic_url in pic_urls:
                        sp = pic_url.split('/')
                        file_name = sp[-1]
                        # print(sp)
                        real_url = 'http:' + pic_url
                        print('正在下载第%s张：%s' % (pic_count, (save_root + '/' + file_name)))
                        # exit(113)
                        request.urlretrieve(real_url, save_root + '/' + file_name)
                        pic_count += 1
                page += 1
            else:
                has_next = False


spider = TmallSpider()
# name = raw_input()
spider.crawl(input('请输入天猫商品的id'), input('输入最大下载页数'))

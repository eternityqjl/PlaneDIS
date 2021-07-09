import requests
from bs4 import BeautifulSoup
import requests
import re
import json
import os
import csv

#----------------------------------------代理配置---------------------------------------------------------------------
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def getHtml(url_getHtml, headers):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url_getHtml, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None
#--------------------------------------------------------------------------------------------------------------------

#testing
if __name__ == '__main__':
    url = 'https://www.planespotters.net/photos/aircraft/Airbus/A300-600'
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    req = getHtml(url, headers)    #获取html源代码
    html = req.text
    bf = BeautifulSoup(html, 'lxml')    #将html源码转换为BeautifulSoup对象

    targets_url = bf.find_all('div', class_='photo_card__grid') #从中提取该页中所有的48张图片的详情页链接
    targets_url1 = targets_url[0].find_all('a') #将所有链接保存到一个list中
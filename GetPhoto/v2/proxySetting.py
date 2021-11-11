import requests
from bs4 import BeautifulSoup

proxypool_url = 'http://127.0.0.1:5555/random'

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()

def getHtml(url, headers):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxy = get_random_proxy()
    proxies = {'http': 'http://' + proxy}
    return requests.get(url, proxies=proxies, headers=headers).text

"""
#测试代理的代码

if __name__ == '__main__':
    url = 'https://www.planespotters.net/photos/aircraft/Airbus/A300-600'
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    html = getHtml(url, headers)    #获取html源代码
    bf = BeautifulSoup(html, 'lxml')    #将html源码转换为BeautifulSoup对象

    targets_url = bf.find_all('div', class_='photo_card__grid') #从中提取该页中所有的48张图片的详情页链接
    targets_url1 = targets_url[0].find_all('a') #将所有链接保存到一个list中
    print(targets_url)
"""
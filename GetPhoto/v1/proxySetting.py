import requests

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
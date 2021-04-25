from proxySetting import *
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
 
url = 'https://www.planespotters.net/photos/aircraft/ATR/ATR-72222'
req = getHtml(url, headers)
html = req.text
print(html)
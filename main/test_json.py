import json
import requests

req = requests.get("http://127.0.0.1:5010/get/").json()

print(req)
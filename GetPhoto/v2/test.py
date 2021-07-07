from bs4 import BeautifulSoup
import requests
import re
import json
import os
import csv

#导入其他模块
from proxySetting import *   #get_proxy, delete_proxy, getHtml
from AircraftType import *

path = '/home/eternityqjl/vscode/PlaneDIS/dataset/Airbus/A300-600'
file_num = len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))])

print(file_num)
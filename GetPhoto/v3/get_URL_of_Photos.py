from bs4 import BeautifulSoup
import re
import os
import csv

import sys 
sys.path.append("..") 
from v2.AircraftType import *
from v2.proxySetting import *


def Parse_pictureURL(manu_name, aircraft_type, url_0):
    
    print(1)

    


if __name__ == '__main__':
    url_0 = 'https://www.planespotters.net/photos/aircraft/'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    print("The number of Manufacturer: %d."%num_manu)   #打印制造商总数
    print("The number of Aircraft type: %d."%num_aircraftType)   #打印机型总数
    print("Start to pasrse URLs of photos of all aircraft types.")


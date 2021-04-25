from bs4 import BeautifulSoup
import requests
import re
import json
import os
import csv

#导入其他模块
from proxySetting import *
from AircraftType import *
#----------------------------创建存放图片的文件夹----------------------------------------------------------------------------
def mkdir(path, each_AircraftType):
    folder = os.path.exists(path)   #判断路径文件夹是否存在的变量
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print("--- New folder: %s ---"%each_AircraftType)
    else:
        print("--- Existing Folder: %s ---"%each_AircraftType)
#----------------------------------------------------------------------------------------------------------------------

#-------------------------------为每个机型创建csv文件--------------------------------------------------------------------------------
def create_csv(path, each_AircraftType):
    csv_filename = '%s.csv'%each_AircraftType
    csv_filename_path = path + '/' + csv_filename
    csv_file = os.path.exists(csv_filename_path)
    if not csv_file:
        with open(csv_filename_path, 'wb') as f:
            writer = csv.writer(f)
            f.close()
        print("--- New csv file: %s ---"%csv_filename)
    else:
        print("--- Existing csv file: %s ---"%csv_filename)
#------------------------------------------------------------------------------------------------------------------------

#-----------------------------写入一行csv，即一张图片的信息-----------------------------------------------------------------------------
def csv_write(path, file_name, plane_airline, plane_type):
    csv_filepath = path + '/' + '%s.csv'%plane_type
    with open(csv_filepath, 'a+') as f:
        csv_write = csv.writer(f)
        data_row = ["%s"%file_name, "%s"%plane_airline, "%s"%plane_type]
        csv_write.writerow(data_row)
        f.close()
#----------------------------------------------------------------------------------------------------------------------------

#def reastart_check():
    


#--------------------------------------download-------------------------------------------------------------------
#下载并保存一张图片
#参数依次表示：图片链接，机型，航司，注册号，保存路径，图片名称
def download(img_url, plane_type, plane_airline, plane_reg, path, name):
    img_url1 = r'%s'%img_url
    req = getHtml(img_url1, headers)   #获取图片

    file_name = path + r'/' + name  #设置图片路径及名称
    f = open(file_name, 'wb')   #创建文件并写入图片
    f.write(req.content)
    f.close

    csv_write(path, file_name, plane_airline, plane_type)   #将图片信息写入csv文件
#-------------------------------------------------------------------------------------------------------------


#-------------------------------------parses_picture------------------------------------------------------------------------
#获取每张图片的cdn链接以及图片信息
def parses_picturePage(url_photo, path):
    url_photo = r'https://www.planespotters.net/' + r'%s'%url_photo   #获取图片详情所在网页url
    img_req = getHtml(url_photo, headers)
    html = img_req.text
    bf = BeautifulSoup(html, 'lxml')    #下载HTML源代码
    try:
        img_url = bf.find('div', class_='photo_large__container').find('img').get('src')    #获取图片地cdn链接(src)
        img_name = bf.find('div', class_='photo_large__container').find('img').get('alt')   #获取图片的完整名称(alt)

        #从完整名称中提取注册号、机型、航司
        #re.findall的返回值是列表list，要将其转换为字符串后使用
        plane_reg = re.findall("^(.*?)\s", img_name)    
        plane_reg = "".join(plane_reg)
        #plane_type = re.findall("ATR\s(.+?)\sphotographed", img_name)
        #plane_type = "".join(plane_type)
        plane_type = "%s"%each_AircraftType
        plane_airline = re.findall("\s(.*?)\s%s"%manu, img_name)
        plane_airline = "".join(plane_airline)

        name = '%d'%n + '_' + plane_type + '_' + plane_airline + '_' + plane_reg + '.jpg'   #生成图片名称

        #下载图片至指定位置
        download(img_url, plane_type, plane_airline, plane_reg, path, name)   #下载图片
        print(u'第%s张图片已下载: %s.' %(n, name))
    except:
        print('Can not get the Photo: %s.'%name)
#--------------------------------------------------------------------------------------------------------------


#-----------------------------------main_circle---------------------------------------------------------------------------
def parse_page(url_page, path, headers):  #下载一个page的48张图片
    global n
    req = getHtml(url_page, headers)    #获取html源代码
    html = req.text
    bf = BeautifulSoup(html, 'lxml')    #将html源码转换为BeautifulSoup对象

    page_url = bf.findall('div', class_='page')
    #targets_page_url = 
    targets_url = bf.find_all('div', class_='photo_card__grid') #从中提取该页中所有的48张图片的详情页链接
    targets_url1 = targets_url[0].find_all('a') #将所有链接保存到一个list中

    for each in targets_url1:   #提取并下载每张图片
        url_photo = each.get('href')
        parses_picturePage(url_photo, path)
        n = n + 1
#------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
#--------------------------------------设置初始化参数-------------------------------------------------------------------------
    url_0 = 'https://www.planespotters.net/photos/aircraft/'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    print("The number of manufacturer: %d."%num_manu)   #打印制造商数量
    print("The number of Aircraft type: %d."%num_all)   #打印机型总数

    #下载一家制造商的所有机型图片(只需修改3处制造商即可:101-103行)
    manu = manufacturer[0]  #制造商名称
    for each_AircraftType in Airbus_AircraftType:
        page_num = Airbus_AircraftType['%s'%each_AircraftType]
        page = list(range(1, page_num+1))

        path = '/home/eternityqjl/vscode/PlaneDIS/dataset/%s/%s'%(manu, each_AircraftType)
#        mkdir(path, each_AircraftType)  #创建存放一个具体机型的文件夹
#        create_csv(path, each_AircraftType) #创建每种机型的csv文件

        n = 1 #每种机型开始的编号数字
        for each_page_num in page:  #循环所有的page，每个page有48张图片
            url_page = url_0 + '%s'%manu + '/' + '%s'%each_AircraftType + '?' + 'page=%d'%each_page_num
            parse_page(url_page, path, headers)   ##下载一个page的48张图片

#---------------------------------------------------------------------------------------------------------------------------
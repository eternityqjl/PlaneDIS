from bs4 import BeautifulSoup
import requests
import re
import json
import os
import csv

#导入其他模块
from proxySetting import *   #get_proxy, delete_proxy, getHtml
from AircraftType import *


#----------------------------创建存放图片的文件夹----------------------------------------------------------------------------
def mkdir(path, each_AircraftType):
    folder = os.path.exists(path)   #判断路径文件夹是否存在的变量
    if not folder:                   #判断是否存在文件夹如果不存在则创建文件夹
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
    if not csv_file:    #检查是否已经存在csv文件
        with open(csv_filename_path, 'wb') as f:
            writer = csv.writer(f)
            f.close()
        print("--- New csv file: %s ---"%csv_filename)
    else:
        print("--- Existing csv file: %s ---"%csv_filename)
#------------------------------------------------------------------------------------------------------------------------

#------------------------检查该机型文件夹，返回仍需的图片数量和下一张图片的编号-------------------------------------------------------------
def check(photo_num, path, each_AircraftType):   #所需图片数量, 路径, 机型


    #检查csv文件中的行数是否与图片数量相等，不相等则按顺序重新创建
    csv_filename = '%s.csv'%each_AircraftType
    csv_filename_path = path + '/' + csv_filename
    with open(csv_filename_path, 'r') as f:
        csv_line_num = len(f.readlines())
    #if photo_num != csv_line_num:

#---------------------------------------------------------------------------------------------------------------------------------

#-----------------------------写入一行csv，即一张图片的信息-----------------------------------------------------------------------------
def csv_write(path, file_name, plane_airline, plane_type):
    csv_filepath = path + '/' + '%s.csv'%plane_type
    with open(csv_filepath, 'a+') as f:
        csv_write = csv.writer(f)
        data_row = ["%s"%file_name, "%s"%plane_airline, "%s"%plane_type]
        csv_write.writerow(data_row)
        f.close()
#----------------------------------------------------------------------------------------------------------------------------
   


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
def parses_picturePage(url_photo, path, next_serial):
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

        name = '%d'%next_serial + '_' + plane_type + '_' + plane_airline + '_' + plane_reg + '.jpg'   #生成图片名称

        #下载图片至指定位置
        download(img_url, plane_type, plane_airline, plane_reg, path, name)   #下载图片
        print(u'第%s张图片已下载: %s.' %(next_serial, name))
    except:
        print('Can not get the Photo: %s.'%name)
#--------------------------------------------------------------------------------------------------------------

#-----------------------------------main_circle---------------------------------------------------------------------------
def parse_page(url_page, path, headers, next_serial):  #下载一个page的48张图片
    #global n
    req = getHtml(url_page, headers)    #获取html源代码
    html = req.text
    bf = BeautifulSoup(html, 'lxml')    #将html源码转换为BeautifulSoup对象

    targets_url = bf.find_all('div', class_='photo_card__grid') #从中提取该页中所有的48张图片的详情页链接
    targets_url1 = targets_url[0].find_all('a') #将所有链接保存到一个list中

    for each in targets_url1:   #提取并下载每张图片
        url_photo = each.get('href')
        parses_picturePage(url_photo, path, next_serial)
        n = n + 1
#------------------------------------------------------------------------------------------------------------------------------

"""
各个url变量：
网站初始量： url_0 = 'https://www.planespotters.net/photos/aircraft/'
每个page： url_page = url_0 + 'ATR' + '/' + '%s'%each_AircraftType + '?' + 'page=%d'%each_page_num
每张图片的详情页： url_photo
图片CDN链接： img_url = bf.find('div', class_='photo_large__container').find('img').get('src')

parse_page -> parse_picturePage -> download
"""

if __name__ == '__main__':
#--------------------------------------设置初始化参数-------------------------------------------------------------------------
    url_0 = 'https://www.planespotters.net/photos/aircraft/'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    print("The number of Manufacturer: %d."%num_manu)   #打印制造商总数
    print("The number of Aircraft type: %d."%num_all)   #打印机型总数

    for manu in manufacturer:   #所有飞机制造商
        for manu_name in manufacturer_name:
            for each_AircraftType in manu:  #一家制造商的所有机型
                path = '/home/eternityqjl/vscode/PlaneDIS/dataset/%s/%s'%(manu_name, each_AircraftType)  #机型文件夹路径
                #首先检查该机型文件夹是否创建，csv文件是否创建，若未创建则先进行创建
                mkdir(path, each_AircraftType)  #创建存放一个具体机型的文件夹
                create_csv(path, each_AircraftType) #创建每种机型的csv文件

                #根据要获取的图片page数量确定所需图片数量
                page_num_origin = manu['%s'%each_AircraftType]
                photo_num_origin = page_num_origin * 48

                file_num = len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))])  #文件数量
                photo_num = file_num - 1    #当前实际图片数量

                #检查csv文件行数与实际图片数量是否对应相等，不相等则重新写入csv

                if photo_num > photo_num_origin:
                    continue
                photo_num_need = photo_num_origin - photo_num   #仍需图片数量
                next_serial = photo_num + 1    #下一张图片的编号

                page_num_end = int(photo_num_need / 48) + 1
                page_num_start = int(photo_num / 48) + 1
                page = list(range(page_num_start, page_num_start+page_num_end+1))   #得到所需图片的page范围

                for each_page_num in page:  #循环所有的page，每个page有48张图片
                    url_page = url_0 + '%s'%manu_name + '/' + '%s'%each_AircraftType + '?' + 'page=%d'%each_page_num
                    parse_page(url_page, path, headers, next_serial)   ##下载一个page的48张图片

#---------------------------------------------------------------------------------------------------------------------------
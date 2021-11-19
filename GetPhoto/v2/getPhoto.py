from bs4 import BeautifulSoup
import re
import os
import csv
#from multiprocessing.pool import Pool, TimeoutError
from pathos.multiprocessing import ProcessPool

#导入其他模块
from proxySetting import getHtml, getPics   #get_proxy, delete_proxy, getHtml
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

#-------------------------------------parses_picture------------------------------------------------------------------------
#获取每张图片的cdn链接以及图片信息
def parses_picture(url_photo, path_dir, next_serial, manu_name, aircraftType_name):
    url_photo = r'https://www.planespotters.net/' + r'%s'%url_photo   #获取图片详情所在网页url
    html = getHtml(url_photo)
    bf = BeautifulSoup(html, 'lxml')    #下载HTML源代码
    try:
        img_url = bf.find('div', class_='photo_large__container').find('img').get('src')    #获取图片地cdn链接(src)
        img_name = bf.find('div', class_='photo_large__container').find('img').get('alt')   #获取图片的完整名称(alt)

        #使用正则表达式从完整名称中提取注册号、机型、航司
        #re.findall的返回值是列表list，要将其转换为字符串后使用
        #有些机型有不同名称，要把庞巴迪CS100和CS300改为空客A220-100和A220-300
        plane_reg = "".join(re.findall("^(.*?)\s", img_name))

        if manu_name=='De_Havilland_Canada':
            plane_airline = "".join(re.findall("\s(.*?)\s%s"%('De-Havilland-Canada'), img_name))
        if manu_name=='McDonnell_Douglas':
            plane_airline = "".join(re.findall("\s(.*?)\s%s"%('McDonnell-Douglas'), img_name))
        if manu_name=='British_Aerospace':
            plane_airline = "".join(re.findall("\s(.*?)\s%s"%('British-Aerospace'), img_name))
        else:
            plane_airline = "".join(re.findall("\s(.*?)\s%s"%manu_name, img_name))

        plane_type = "%s"%aircraftType_name

        name = '%d'%next_serial + '_' + plane_type + '_' + plane_airline + '_' + plane_reg + '.jpg'   #生成图片名称

        #下载图片至指定位置
        img_url1 = r'%s'%img_url
        req = getPics(img_url1)   #获取图片
        file_name = path_dir + r'/' + name  #设置图片路径及名称
        f = open(file_name, 'wb')   #创建文件并写入图片
        f.write(req.content)
        f.close
        csv_write(path_dir, file_name, plane_airline, plane_type)   #将图片信息写入csv文件
        print(u'%s: 第%s张图片已下载: %s.' %(plane_type, next_serial, name))
    except:
        print('Can not get the Photo: %s.'%name)
#--------------------------------------------------------------------------------------------------------------

#-----------------------------------main_circle---------------------------------------------------------------------------
#下载一个page的48张图片
def parse_page(url_page, path_dir, next_serial, manu_name, AircraftType_name):
    html = getHtml(url_page)    #获取html源代码
    bf = BeautifulSoup(html, 'lxml')    #将html源码转换为BeautifulSoup对象

    targets_url = bf.find_all('div', class_='photo_card__grid') #从中提取该页中所有的48张图片的详情页链接
    targets_url1 = targets_url[0].find_all('a') #将所有链接保存到一个list中

    for each in targets_url1:   #提取并下载每张图片
        url_photo = each.get('href')
        parses_picture(url_photo, path_dir, next_serial, manu_name, AircraftType_name)
        next_serial = next_serial + 1

    return next_serial
#------------------------------------------------------------------------------------------------------------------------------


def main_process(manu_name, AircraftType_name, page_num):
    #机型文件夹路径
    path_dir = '/home/eternityqjl/projects/PlaneDIS/dataset/%s/%s'%(manu_name, AircraftType_name) 

    #首先检查该机型文件夹是否创建，csv文件是否创建，若未创建则先进行创建
    mkdir(path_dir, AircraftType_name)  #创建存放一个具体机型的文件夹
    create_csv(path_dir, AircraftType_name) #创建每种机型的csv文件

    #根据要获取的图片page数量确定所需图片数量
    photo_num_origin = page_num * 48     #所需图片数量
    file_num = len([lists for lists in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, lists))])  #文件数量
    photo_num = file_num - 1    #当前实际图片数量

    #检查是否已经下载足够数量图片,并且确定下一张图片的编号
    if photo_num >= photo_num_origin:
        print("%s: enough photos. Total number: %d."%(AircraftType_name, photo_num))
        return
    photo_num_need = photo_num_origin - photo_num   #仍需图片数量
    next_serial = photo_num + 1    #下一张图片的编号

    #得到所需图片的page范围
    page_num_end = int(photo_num_origin / 48) + 2
    page_num_start = int(photo_num / 48) + 2
    page = list(range(page_num_start, page_num_end+1))   

    #循环所有的page，每个page有48张图片
    for each_page_num in page:
        url_page = url_0 + '%s'%manu_name + '/' + '%s'%AircraftType_name + '?' + 'page=%d'%each_page_num
        next_serial = parse_page(url_page, path_dir, next_serial, manu_name, AircraftType_name)   ##下载一个page的48张图片


def create_para_list():
    list1 = []
    manufacturer_name = list(manufacturer)
    #三级：制造商-机型-page数量
    for manu_name in manufacturer_name:
        x1 = manufacturer[manu_name]    #一个制造商所有机型的键值对
        aircraftType_name = list(x1)
        for each_aircraftType_name in aircraftType_name:
            list1.append(['%s'%manu_name, '%s'%each_aircraftType_name, x1[each_aircraftType_name]])
    return list1

if __name__ == '__main__':
#--------------------------------------设置初始化参数-------------------------------------------------------------------------
    url_0 = 'https://www.planespotters.net/photos/aircraft/'

    print("The number of Manufacturer: %d."%num_manu)   #打印制造商总数
    print("The number of Aircraft type: %d."%num_aircraftType)   #打印机型总数

    list0 = create_para_list()


    para = [[p[0] for p in list0], [p[1] for p in list0], [p[2] for p in list0]]

    #main_process("Bombardier", "CRJ-700", 20)

    with ProcessPool(nodes=15) as pool:
        result = pool.map(main_process, para[0], para[1], para[2])
        try:
            print(result.get(timeout=10))
        except TimeoutError:
            print(TimeoutError.__name__)

#---------------------------------------------------------------------------------------------------------------------------
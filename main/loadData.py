import os
import sys
import glob
import csv

#direc = listdir(path='/home/eternityqjl/vscode/PlaneDIS/dataset/*/*')
path = glob.glob('/home/eternityqjl/vscode/PlaneDIS/dataset/*/*/*.csv')
print(path)


"""
with open(path0, 'wb') as f:
    writer = csv.writer(f)
    f.close()

#每张图片的路径

print(path[0])

print(sys.path[0])
source_path = sys.path[0] + '\\filename.xls'
"""
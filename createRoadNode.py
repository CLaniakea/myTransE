'''
将时间提取出来建立entityRoad.txt
格式:
name num
'''
import os
import csv

file_dir = "./data/roads.txt"
dst_dir = "./data/entityRoad.txt"

count = 0
with open(dst_dir, 'w', encoding='UTF-8') as dst:
    with open(file_dir, encoding='UTF-8') as f:
        reader = f.readlines()
        for line in reader:
            line = line.strip('\n')
            list = line.split(',')
            dst.writelines(list[1]+'\t'+str(count)+'\n')
            count += 1
            if count % 1000 == 0:
                print(count)

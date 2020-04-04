'''
将时间提取出来建立entityTime.txt
'''
import os
import csv

file_dir = "./data/TSOctober1225.txt"
dst_dir = "./data/entityTime.txt"

count = 4089
with open(dst_dir, 'w+', encoding='UTF-8') as dst:
    with open(file_dir, encoding='UTF-8') as f:
        reader = f.readlines()
        for line in reader:
            line = line.strip('\n')
            list = line.split(',')
            count += 1
            dst.writelines(list[-1] + '\t' + str(count) + '\n')
            if count % 1000 == 0:
                print(count)

import os
import pandas as pd
from datetime import datetime
'''
从三元组中寻找一些周期关系
'''

data_dir = './data/'
file_name = 'testall.txt'
dst_dir = './data/foundrule.txt'
load_relation = pd.read_table(os.path.join('./data', 'relation2id.txt'), header=None)
relation2idDict = dict(zip(load_relation[0], load_relation[1]))
entity_road = pd.read_table(os.path.join(data_dir, file_name), header=None)
tuple_list = list(zip(entity_road[0], entity_road[1], entity_road[2]))
# print(tuple_list[0][0])
# head_entity_dict = {}
# tail_entity_dict = {}
# relation_dict = {}
'''
计算八一路在一周内路况
'''

weeklist = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
def test(road_name):
    # L = [0, 0, 0, 0, 0]#记录各个路况出现的次数
    L_PLUS = [[0]*5 for i in range(7)]
    count = 0#总路况数
    f = open(dst_dir, 'a+', encoding = 'UTF-8')
    for tp in tuple_list:
        if tp[0] == road_name:
            temp = list(tp[1].split(' '))[0]
            week = datetime.strptime(temp, "%Y-%m-%d").weekday() #返回0 - 6
            # print(weeklist[week])
            # L[relation2idDict[tp[2]]] += 1
            L_PLUS[week][relation2idDict[tp[2]]] += 1
            count += 1
            tp = tp + tuple(weeklist[week])
            # break
    f.write(road_name + '\n')
    for L in L_PLUS:
        for x in L:
            f.write(str(round(x/count, 2)) + '\t')
        f.write('\n')
    f.close()

road_list = []# 不重复的路名
for tp in tuple_list:
    if tp[0] not in road_list:
        road_list.append(tp[0])
        # print(tp[0])
print("the number of roads ", len(road_list))
for name in road_list:
    print(name)
    test(name)

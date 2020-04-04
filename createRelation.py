# import os
# import pandas as pd

# '''
# 创建关系：Road Time Type
# '''
# data_dir = './data'
# road_dict_file = 'entityRoad.txt'
# time_dir = './data/TSOctober1225.txt'
# dst_dir = './data/train.txt'
# valid_dir = './data/valid.txt'
# test_dir = './data/test.txt'


# print("------loading road file------")
# entity_road = pd.read_table(os.path.join(data_dir, road_dict_file), header=None)
# print("------finish load road file")
# road_dict = dict(zip(entity_road[0], entity_road[1]))
# # print(road_dict)
# load_relation = pd.read_table(os.path.join(data_dir, 'relation2id.txt'), header=None)
# relation_dict = dict(zip(load_relation[0], load_relation[1]))
# # print(road_dict[2459])

# # print('２０２国道' in road_dict)
# print(relation_dict)
# count = 0
# with open(valid_dir, 'w', encoding='UTF-8') as v:
#     with open(test_dir, 'w', encoding='UTF-8') as t:
#         with open(time_dir, encoding='UTF-8') as f:
#             with open(dst_dir, 'w', encoding='UTF-8') as dst:
#                 reader = f.readlines()
#                 for line in reader:
#                     line = line.strip('\n')
#                     list_type = line.split(',')
#                     list_road_name = line.split('：')
#                     if list_road_name[0] in road_dict:
#                         if count == 8:
#                             v.writelines(list_road_name[0] + '\t' + list_type[-1] + '\t' + list_type[-3] + '\n')
#                         elif count == 9:
#                             t.writelines(list_road_name[0] + '\t' + list_type[-1] + '\t' + list_type[-3] + '\n')
#                         else:
#                             dst.writelines(list_road_name[0] + '\t' + list_type[-1] + '\t' + list_type[-3] + '\n')
#                         count = (count + 1) % 10
#                     else:
#                         continue


#创建 最后一天的测试文件
import os
import pandas as pd

'''
创建关系：Road Time Type
'''
data_dir = './data'
road_dict_file = 'entityRoad.txt'
time_dir = './data/TSOctober1225.txt'
# dst_dir = './data/train.txt'
# valid_dir = './data/valid.txt'
test_dir = './data/testlast.txt'


print("------loading road file------")
entity_road = pd.read_table(os.path.join(data_dir, road_dict_file), header=None)
print("------finish load road file")
road_dict = dict(zip(entity_road[0], entity_road[1]))
# print(road_dict)
load_relation = pd.read_table(os.path.join(data_dir, 'relation2id.txt'), header=None)
relation_dict = dict(zip(load_relation[0], load_relation[1]))
# print(road_dict[2459])

# print('２０２国道' in road_dict)
print(relation_dict)
count = 0
with open(test_dir, 'w', encoding='UTF-8') as t:
    with open(time_dir, encoding='UTF-8') as f:
        reader = f.readlines()
        for line in reader:
            line = line.strip('\n')
            list_type = line.split(',')
            list_road_name = line.split('：')
            if list_road_name[0] in road_dict:
                # if count == 8:
                #     v.writelines(list_road_name[0] + '\t' + list_type[-1] + '\t' + list_type[-3] + '\n')
                # elif count == 9:
                t.writelines(list_road_name[0] + '\t' + list_type[-1] + '\t' + list_type[-3] + '\n')
                # else:
                #     dst.writelines(list_road_name[0] + '\t' + list_type[-1] + '\t' + list_type[-3] + '\n')
                # count = (count + 1) % 10
            else:
                continue
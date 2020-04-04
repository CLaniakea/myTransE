import os

dst_file = './data/relation2id.txt'

count = 0
list = ['畅通', '基本畅通', '行驶缓慢', '拥堵', '严重拥堵']
with open(dst_file, 'w', encoding='UTF-8') as dst:
    for one in list:
        dst.writelines(one + '\t' + str(count) + '\n')
        count += 1
'''
找到爬取的道路交通态势其road_id
找到与之对应的事时间序号及时间，写入roads_re_time1225.csv
'''

import os
import csv
#之前使用neo4j-import时使用过，作废
# dst_dir = "C:\\Users\\15866\\Desktop\\毕设\\TS\\roads_re_time1225.csv"
# dir = "C:\\Users\\15866\\Desktop\\毕设\\TS\\TSOctober1225.txt"
# roads_dir = "C:\\Users\\15866\\Desktop\\dest\\data\\roads.txt"
# # dst_dir = "C:\\Users\\15866\\Desktop\\毕设\\TS\\find_road_id.txt"
# # list = os.listdir(dir)
# dst = []
# count = 0  #tag
# with open(dst_dir, 'w', newline="") as dst_csv:
#     csv_writer = csv.writer(dst_csv, dialect='excel')
#     csv_writer.writerow([":START_ID", ":END_ID", ":TYPE"])
#     with open(roads_dir, encoding='UTF-8') as rf:
#         rfreader = rf.readlines()
#         with open(dir, encoding='UTF-8') as f:
#             freader = f.readlines()
#             for line in freader:
#                 line = line.strip('\n')
#                 list = line.split('：')
#                 for rfline in rfreader:
#                     rfline = rfline.strip('\n')
#                     rflist = rfline.split(',')
#                     if list[0] == rflist[1]:
#                         count += 1
#                         another_list = line.split(',')
#                         # d.writelines(rflist[0] + ',' + list[0] + ',' + another_list[6] + ',' + another_list[8] + '\n')
#                         # print([rflist[0]] + [rflist[1]] + [another_list[6]] + [count] + [another_list[8]])

#                         csv_writer.writerow([rflist[0]] + ["t" + str(count)] + [another_list[6]])
#                         if count % 100 == 0:
#                             print(count)
#                         break

                # print(list)
                # break

'''
LOAD CSV
'''

dst_dir1 = "C:\\Users\\15866\\Desktop\\毕设\\TS\\re1225畅通.csv"
dst_dir2 = "C:\\Users\\15866\\Desktop\\毕设\\TS\\re1225基本畅通.csv"
dst_dir3 = "C:\\Users\\15866\\Desktop\\毕设\\TS\\re1225行驶缓慢.csv"
dst_dir4 = "C:\\Users\\15866\\Desktop\\毕设\\TS\\re1225拥堵.csv"
dst_dir5 = "C:\\Users\\15866\\Desktop\\毕设\\TS\\re1225严重拥堵.csv"

dir = "C:\\Users\\15866\\Desktop\\毕设\\TS\\TSOctober1225.txt"
roads_dir = "C:\\Users\\15866\\Desktop\\dest\\data\\roads.txt"
# dst_dir = "C:\\Users\\15866\\Desktop\\毕设\\TS\\find_road_id.txt"
# list = os.listdir(dir)
dst = []
count = 0  #tag
with open(dst_dir1, 'w', newline="") as dst_csv1:
    csv_writer1 = csv.writer(dst_csv1, dialect='excel')
    csv_writer1.writerow(["road_id", "time_id"])
    with open(dst_dir2, 'w', newline="") as dst_csv2:
        csv_writer2 = csv.writer(dst_csv2, dialect='excel')
        csv_writer2.writerow(["road_id", "time_id"])
        with open(dst_dir3, 'w', newline="") as dst_csv3:
            csv_writer3 = csv.writer(dst_csv3, dialect='excel')
            csv_writer3.writerow(["road_id", "time_id"])
            with open(dst_dir4, 'w', newline="") as dst_csv4:
                csv_writer4 = csv.writer(dst_csv4, dialect='excel')
                csv_writer4.writerow(["road_id", "time_id"])
                with open(dst_dir5, 'w', newline="") as dst_csv5:
                    csv_writer5 = csv.writer(dst_csv5, dialect='excel')
                    csv_writer5.writerow(["road_id", "time_id"])

                    with open(roads_dir, encoding='UTF-8') as rf:
                        rfreader = rf.readlines()
                        with open(dir, encoding='UTF-8') as f: #Time File
                            freader = f.readlines()
                            for line in freader:
                                line = line.strip('\n')
                                list = line.split('：')
                                for rfline in rfreader:
                                    rfline = rfline.strip('\n')
                                    rflist = rfline.split(',')
                                    if list[0] == rflist[1]:
                                        count += 1
                                        another_list = line.split(',')
                                        if another_list[6] == '畅通':
                                            csv_writer1.writerow([rflist[0]] + [str(count)])
                                        elif another_list[6] == '基本畅通':
                                            csv_writer2.writerow([rflist[0]] + [str(count)])
                                        elif another_list[6] == '行驶缓慢':
                                            csv_writer3.writerow([rflist[0]] + [str(count)])    
                                        elif another_list[6] == '拥堵':
                                            csv_writer4.writerow([rflist[0]] + [str(count)])
                                        elif another_list[6] == '严重拥堵':
                                            csv_writer5.writerow([rflist[0]] + [str(count)])

                                        if count % 100 == 0:
                                            print(count)
                                        break


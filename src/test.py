from numpy import *
import operator
import pandas as pd
import os

class Test:
    def __init__(self, entityList, entityVectorList,
                 relationList, relationVectorList,
                 tripleListTrain, tripleListTest,
                 label="head", isFit=False
                 ):
        self.entityDict = {}
        self.relationDict = {}
        self.relation2idDict = {}
        for name, vec in zip(entityList, entityVectorList):
            self.entityDict[name] = vec
            # print(self.entityDict)
        for name, vec in zip(relationList, relationVectorList):
            self.relationDict[name] = vec
        # 建立字典{'name': vec(all of values)}
        load_relation = pd.read_table(os.path.join('../data', 'relation2id.txt'), header=None)
        self.relation2idDict = dict(zip(load_relation[0], load_relation[1]))

        self.tripleListTrain = tripleListTrain
        self.tripleListTest = tripleListTest
        self.rank = []
        self.label = label
        self.isFit = isFit

    def writeRank(self, dir):
        print("写入")
        file = open(dir, 'w')
        for r in self.rank:
            file.write(str(r[0]) + "\t")
            file.write(str(r[1]) + "\t")
            file.write(str(r[2]) + "\t")
            file.write(str(r[3]) + "\n")
        file.close()

    def getRank(self):
        cou = 1
        length = len(self.tripleListTest)
        for triplet in self.tripleListTest:
            rankList = {}  # '路名': distance
            for entityTemp in self.entityDict.keys():
                if self.label == "head":
                    corruptedTriplet = (entityTemp, triplet[1], triplet[2])
                    # 当前entityTemp与时间，路况构成的三元组
                    if self.isFit and (corruptedTriplet in self.tripleListTrain):
                        continue
                    rankList[entityTemp] = distance(self.entityDict[entityTemp],
                                                    self.entityDict[triplet[1]],
                                                    self.relationDict[triplet[2]])
                    # print(rankList)
                else:  #
                    corruptedTriplet = (triplet[0], entityTemp, triplet[2])
                    if self.isFit and (corruptedTriplet in self.tripleListTrain):
                        continue
                    rankList[entityTemp] = distance(self.entityDict[triplet[0]],
                                                    self.entityDict[entityTemp],
                                                    self.relationDict[triplet[2]])
            nameRank = sorted(rankList.items(), key=operator.itemgetter(1))  # 按照distance排序
            # print("nameRank =", nameRank)
            if self.label == 'head':
                numTri = 0
            else:
                numTri = 1
                # ('昆明街', '2019-12-25 10:30', '畅通')--元组头，元组尾
            x = 1
            for i in nameRank:
                if i[0] == triplet[numTri]:
                    break
                x += 1
            # x-1 是路名 triplet[0]即头实体在nameRank中的下标
            print("len(nameRank) =", len(nameRank))
            print(triplet, triplet[numTri], nameRank[0][0], x)
            self.rank.append((triplet, triplet[numTri], nameRank[0][0], x))
            # print("x =", x)
            # print("namerankx-1 =", nameRank[x-1])
            print("---TESTING---:", cou, "/", length, "sub =", x)
            # x > len 说明没找到
            cou += 1
            # if cou % 10000 == 0:
            #     print("cou =", cou)

    def getRelationRank(self):
        correctCount = 0
        cou = 1
        hits2 = 0
        length = len(self.tripleListTest)
        self.rank = []
        for triplet in self.tripleListTest:
            rankList = {}
            for relationTemp in self.relationDict.keys():
                corruptedTriplet = (triplet[0], triplet[1], relationTemp)
                if self.isFit and (corruptedTriplet in self.tripleListTrain):
                    continue
                rankList[relationTemp] = distance(self.entityDict[triplet[0]],
                                                  self.entityDict[triplet[1]],
                                                  self.relationDict[relationTemp])
            nameRank = sorted(rankList.items(), key=operator.itemgetter(1))  # type List
            # print(rankList)
            # print(type(rankList))
            x = 1
            for i in nameRank:
                if i[0] == triplet[2]:
                    break
                x += 1
            self.rank.append((triplet, triplet[2], nameRank[0][0], x))

            # print(self.relation2idDict)
            # print(abs(self.relation2idDict[triplet[2]] - self.relation2idDict[nameRank[0][0]]))
            correctCount += (abs(self.relation2idDict[triplet[2]] - self.relation2idDict[nameRank[0][0]]) <= 1)
            # correctCount += (triplet[2] == nameRank[0][0])

            print("---TESTING---:", cou, "/", length, "sub =", x)
            hits2 += (x <= 2)
            cou += 1
        print("---正确率--- ", round(float(correctCount / cou) * 100, 2), "%")
        print("---@hits2--- ", round(float(hits2 / cou) * 100, 2), "%")
        # 原来的关系在排序之后的第 x 个
        # if cou % 10000 == 0:
        #     print(cou)

    def getMeanRank(self):
        num = 0
        for r in self.rank:
            num += r[3]
        return num / len(self.rank)
        # getRank(self): x


def distance(h, t, r):
    h = array(h)
    t = array(t)
    r = array(r)
    s = h + r - t
    return linalg.norm(s)


def openD(dir, sp="\t"):
    # triple = (head, tail, relation)
    num = 0
    list = []
    with open(dir, encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
            triple = line.strip().split(sp)
            if (len(triple) < 3):
                continue
            list.append(tuple(triple))
            num += 1
    print(num)
    return num, list


def loadData(str):
    fr = open(str)
    sArr = [line.strip().split("\t") for line in fr.readlines()]
    datArr = [[float(s) for s in line[1][1:-1].split(", ")] for line in sArr]
    nameArr = [line[0] for line in sArr]
    return datArr, nameArr


if __name__ == '__main__':

    data_dir = '../data/'
    peroid_file = 'foundrule.txt'
    period_dict ={}
    with open(data_dir + peroid_file, encoding='UTF-8') as fp:
        reader = fp.readlines()
        for read in reader:
            x = read.split('\t')[0]
            y = [int(s) for s in read.split('\t')[1][1:-1].split(',')]
            z = int(read.split('\t')[2])
            y = [round(s/z,2) for s in y]
            period_dict[x] = y
    print(period_dict)

    #
    # dirTrain = "../data/train.txt"
    # tripleNumTrain, tripleListTrain = openD(dirTrain)  # train内容个数 + 元组
    # dirTest = "../data/testlast.txt"#1.15测试
    # # dirTest = "../data/test.txt"#随机测试
    # tripleNumTest, tripleListTest = openD(dirTest)  # test内容个数 + 元组
    # # print("tripleNumTest =", tripleNumTest)
    # # print("tripleListTest =", tripleListTest)
    # dirEntityVector = "../data/result/entityVector.txt"
    # entityVectorList, entityList = loadData(dirEntityVector)  # 前者数据，后者路名
    # # print("entityVectorList =", entityVectorList[0])
    # # print("entityList =", entityList[0])
    # dirRelationVector = "../data/result/relationVector.txt"
    # relationVectorList, relationList = loadData(dirRelationVector)  # 前者数据，后者路况
    # print("START TEST")
    # '''
    # RAW
    # '''
    # testHeadRaw = Test(entityList, entityVectorList,
    #                    relationList, relationVectorList,
    #                    tripleListTrain, tripleListTest)
    # testHeadRaw.getRelationRank()
    # print("HeadRawMeanRank:", testHeadRaw.getMeanRank())
    # testHeadRaw.writeRank("../data/result/" + "testRelationRaw" + ".txt")
    #

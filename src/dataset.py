import os
import pandas as pd
import numpy as np
import random


class KnowledgeGraph:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.entity_dict = {}
        self.entities = []
        self.relation_dict = {}
        self.n_entity = 0
        self.n_relation = 0
        self.training_triples = []  # list of triples in the form of (h, t, r)
        self.validation_triples = []
        self.test_triples = []
        self.n_training_triple = 0
        self.n_validation_triple = 0
        self.n_test_triple = 0
        '''load dicts and triples'''
        self.load_dicts()
        self.load_triples()
        '''construct pools after loading'''
        self.training_triple_pool = set(self.training_triples)
        self.golden_triple_pool = set(self.training_triples) | set(self.validation_triples) | set(self.test_triples)

    def load_dicts(self):
        entity_dict_file = 'entity2id.txt'
        relation_dict_file = 'relation2id.txt'
        print('-----Loading entity dict-----')
        entity_df = pd.read_table(os.path.join(self.data_dir, entity_dict_file), header=None)
        # print("--test1", entity_df)
        '''like:
           0   1
        0  xxx 0
        1  xxx 1
        ...   ...
        #可以按列提取 entity_df[0], entity_df[1]
        '''
        '''
        read_table: 从文件、url、文件型对象中加载带分隔符的数据，默认为'\t'
        header = None: 示txt文件的第一行不是列的名字，是数据。若不写，则读入txt数据时，会没了第一行
        '''
        self.entity_dict = dict(zip(entity_df[0], entity_df[1]))#转元组 转列表 转dict
        # print("--test2",self.entity_dict)
        '''
        [14951 rows x 2 columns]
        {'/m/06rf7': 0, '/m/0c94fn': 1, '/m/016ywr': 2, ......}
        '''
        self.n_entity = len(self.entity_dict)
        # print("--test3", self.n_entity)
        self.entities = list(self.entity_dict.values())# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...]
        # print(self.entities)
        print('#entity: {}'.format(self.n_entity))
        print('-----Loading relation dict-----')
        relation_df = pd.read_table(os.path.join(self.data_dir, relation_dict_file), header=None)
        self.relation_dict = dict(zip(relation_df[0], relation_df[1]))
        self.n_relation = len(self.relation_dict)
        print('#relation: {}'.format(self.n_relation))

    def load_triples(self):
        training_file = 'train.txt'
        validation_file = 'valid.txt'
        test_file = 'test.txt'
        print('-----Loading training triples-----')
        training_df = pd.read_table(os.path.join(self.data_dir, training_file), header=None)
        # print("--test4", training_df)
        '''
        train.txt 文件有三列，此为分别读取各列，格式如上
        '''
        self.training_triples = list(zip([self.entity_dict[h] for h in training_df[0]],
                                         [self.entity_dict[t] for t in training_df[1]],
                                         [self.relation_dict[r] for r in training_df[2]]))
        #  <zip object at 0x0000020EFB7D4BC8>为zip返回，加list转list
        # print("--test5", self.training_triples)
        self.n_training_triple = len(self.training_triples)
        print('#training triple: {}'.format(self.n_training_triple))
        print('-----Loading validation triples-----')
        validation_df = pd.read_table(os.path.join(self.data_dir, validation_file), header=None)
        self.validation_triples = list(zip([self.entity_dict[h] for h in validation_df[0]],
                                           [self.entity_dict[t] for t in validation_df[1]],
                                           [self.relation_dict[r] for r in validation_df[2]]))
        self.n_validation_triple = len(self.validation_triples)
        print('#validation triple: {}'.format(self.n_validation_triple))
        print('-----Loading test triples------')
        test_df = pd.read_table(os.path.join(self.data_dir, test_file), header=None)
        self.test_triples = list(zip([self.entity_dict[h] for h in test_df[0]],
                                     [self.entity_dict[t] for t in test_df[1]],
                                     [self.relation_dict[r] for r in test_df[2]]))
        self.n_test_triple = len(self.test_triples)
        print('#test triple: {}'.format(self.n_test_triple))

    def next_raw_batch(self, batch_size):
        rand_idx = np.random.permutation(self.n_training_triple)
        # n_training_triple = 483142, 对 0-483141 随机打乱
        start = 0
        while start < self.n_training_triple:
            # print("--test6 start = ", start)
            end = min(start + batch_size, self.n_training_triple)
            yield [self.training_triples[i] for i in rand_idx[start:end]]
            start = end
        # 随机打乱取数据

    def generate_training_batch(self, in_queue, out_queue):
        while True:
            raw_batch = in_queue.get()
            if raw_batch is None:
                return
            else:
                batch_pos = raw_batch # positive
                batch_neg = [] # negative
                corrupt_head_prob = np.random.binomial(1, 0.5)# 二项分布
                for head, tail, relation in batch_pos:
                    head_neg = head
                    tail_neg = tail
                    while True:
                        if corrupt_head_prob:
                            head_neg = random.choice(self.entities)
                        else:
                            tail_neg = random.choice(self.entities)
                        if (head_neg, tail_neg, relation) not in self.training_triple_pool:
                            break
                    batch_neg.append((head_neg, tail_neg, relation))
                out_queue.put((batch_pos, batch_neg))

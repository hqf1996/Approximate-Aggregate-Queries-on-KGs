# -*- coding: utf-8 -*-
import config
import models
import tensorflow as tf
import numpy as np
import json
import os
import codecs
import time
import sys

def main(argv):
    iteration_num = 500
    dimension = 200
    # dimension = 100

    con = config.Config()
    con.set_in_path("./benchmarks/experiment/DBpedia/")


    con.set_work_threads(4)
    con.set_dimension(dimension)
    con.set_import_files("./my/experimentModel/transE/dbpedia_PartOfGraph/allDataNoType/iteration%d/%d/model.vec.tf" % (iteration_num, dimension))

    con.init()
    con.set_model(models.TransE)

    # 打印关系之间的相似度
    relation_file = codecs.open(os.path.join(con.in_path, "relation2id.txt"), "r", encoding='utf-8')
    count = int(relation_file.readline().strip())
    d = list()
    for line in relation_file:
        d.append(line.split('\t')[0])

    head = argv[1]
    type = argv[2]

    entity_file = codecs.open(os.path.join(con.in_path, "entity2id.txt"), "r", encoding='utf-8')
    relation_file = codecs.open(os.path.join(con.in_path, "relation2id.txt"), "r", encoding='utf-8')
    subgraph_file = codecs.open("/root/myOpenKE/EAQ_result/subGraph/dbpedia/California_software.txt", "r", encoding='utf-8')

    count = int(entity_file.readline().strip())
    count_relation = int(relation_file.readline().strip())
    d1 = {}  # String_id -->int
    d2 = {}  # name -->int
    for line in entity_file:
        arr = line.split('\t')
        String_id = arr[0].split(' ')[1]
        String_name = arr[0].split(' ')[0]
        iid = int(arr[1])
        d1[String_id] = iid
        d2[String_name] = iid
    d_relation = {}
    for line in relation_file:
        arr = line.split('\t')
        iid = int(arr[1])
        d_relation[arr[0]] = iid
    d_subgraph = {}  # String_id--->int
    index_subgraph_type = list()  # 存放所有类型满足条件的index
    index_subgraph_allType = list()  # 存放所有框定的节点
    for line in subgraph_file:
        arr = line.split('\t')
        d_subgraph[arr[0]] = d1[arr[0]]
        if arr[1].split("\r\n")[0] == type:
            index_subgraph_type.append(d1[arr[0]])
        index_subgraph_allType.append(d1[arr[0]])
    print len(index_subgraph_type)

    Automobile_dict = {}

    while True:
        ip = input("input ")
        # 对范围内所有点计算距离，然后反比即为概率pi
        start1 = time.time()
        entity_vec = con.get_parameters("numpy")["ent_embeddings"]
        startNode = entity_vec[d2[head]]

        pi = {}
        AllValue = list()  # 用于后续归一化找最大最小值
        for index in index_subgraph_allType:
            dis = np.linalg.norm(startNode - entity_vec[index])
            if dis == 0:
                pi_each = 0
            else:
                pi_each = 1.0/dis
            pi[index] = pi_each
            AllValue.append(pi_each)
        maxV = max(AllValue)
        minV = min(AllValue)
        chazhi = maxV-minV
        # 归一化处理
        for each in pi:
            pi[each] = (pi[each]-minV) / chazhi

        sss = time.time()
        # 开始计算COUNT
        piLine = 0.3
        aDic = {}
        bDic = {}
        for each in pi:
            # a要大于某一阈值，并且是目标点
            if pi[each] > piLine and each in index_subgraph_type:
                aDic[each] = pi[each]
            # 考虑b取目标实体
            if each in index_subgraph_type:
                bDic[each] = pi[each]
        sumA_fenzi = 0
        sumA_fenmu = 0
        sumB = 0
        for each in aDic:
            if each in Automobile_dict.keys():
                val = Automobile_dict[each].leng
            else:
                val = 0
            if 100 <= val <= 1000:
                sumA_fenzi += aDic[each] * 1
            # sumA_fenzi += aDic[each] * 1
            sumA_fenmu += aDic[each]
        for each in bDic:
            sumB += bDic[each]
        COUNT_res = sumA_fenzi/(sumA_fenmu/sumB)
        print "COUNT = %lf" % COUNT_res
        eee = time.time()
        print "sum time is: %lf\n" % (eee - sss)
        print "Tile sum time is: %lf\n" % (eee - start1)


        # 计算SUM
        piLine = 0.3
        aDic = {}
        bDic = {}
        for each in pi:
            # a要大于某一阈值，并且是目标点
            if pi[each] > piLine and each in index_subgraph_type:
                aDic[each] = pi[each]
            # 考虑b取目标实体
            if each in index_subgraph_type:
                bDic[each] = pi[each]
        sumA_fenzi = 0
        sumA_fenmu = 0
        sumB = 0
        for each in aDic:
            # pri = 0
            # horsepower = 0
            # total_box_office = 0
            # people = 0
            # age = 0
            leng = 0
            val = 0
            sumA_fenmu += aDic[each]
        for each in bDic:
            sumB += bDic[each]
        res = sumA_fenzi/(sumA_fenmu/sumB)
        print "Ground-truth : %lf" % 124
        print "---------------------------------------------"
        print "Approximate result : %lf" % res
        print "Relative error (%) : %lf" % (100.0*(124-res)/124)
        print "---------------------------------------------"
        end = time.time()
        print "Response Time (ms) : %lf\n" % (end - start1)


if __name__ == '__main__':
    main(sys.argv)
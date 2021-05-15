# -*- encoding:utf-8 -*-
# -*- encoding:utf-8 -*-
from math import log
import random
import numpy as np
import os
import datetime


def KLD(p, q):     #计算KL散度
    p += np.spacing(1)
    q += np.spacing(1)
    # print(p/q)
    return sum([_p * log(_p/_q) for (_p,_q) in zip(p,q)])


def JSD_core(p, q): #计算JS散度（Jensen–Shannon divergence）

    M = [0.5 * (_p + _q) for _p, _q in zip(p, q)]

    # p = p + np.spacing(1)
    # q = q + np.spacing(1)
    return 0.5 * KLD(p, M) + 0.5 * KLD(q, M)


def main():
    min_latitude = 39.6
    min_longitude = 115.8
    len_latitude = 1.2
    len_longitude = 1.6
    wei = len_latitude / 6
    jing = len_longitude / 6
    A = 36


    RD = np.zeros(A*A)
    RSD = np.zeros(A*A)
    D = []
    SD = []
    path_all = []
    base_path_list = os.listdir('../data/Geolife Trajectories 1.3/Trajectories7000/')
    for path in base_path_list:
        file_object = open('../data/Geolife Trajectories 1.3/Trajectories7000/' + path, 'r')
        T0 = []
        path_all.append(path)
        for line in file_object.readlines():
            jw = line.strip().split(',')
            w = jw[0].strip()
            w = float(w)
            w = int((w-min_latitude) / wei)
            j = jw[1].strip()
            j = float(j)
            j = int((j-min_longitude) / jing)
            print(w, j)
            T0.append(w * 6 + j)
        D.append(T0)
        # print(T0[0]*A+T0[-1])
        RD[T0[0]*A+T0[-1]] += 1
        # print(T0)
    print(RD)


    path_all = []
    base_path_list = os.listdir("../data/Geolife Trajectories 1.3/test/3/")
    for path in base_path_list:
        file_object = open(r"../data/Geolife Trajectories 1.3/test/3/" + path, 'r')
        T0 = []
        path_all.append(path)
        for line in file_object.readlines():
            jw = line.strip().split(',')
            w = jw[0].strip()
            w = float(w)
            w = int((w - min_latitude) / wei)
            j = jw[1].strip()
            j = float(j)
            j = int((j - min_longitude) / jing)
            if w * 6 + j <= 35:
                T0.append(w * 6 + j)
        if T0:
            SD.append(T0)
            # print(T0[0]*A+T0[-1])
            print(T0[0], T0[-1])
            print(T0[0] * A + T0[-1])
            try:
                RSD[T0[0] * A + T0[-1]] += 1
            except:
                continue
            # print(T0)
    print(RSD)

    RD = RD / np.sum(RD)
    RSD = RSD / np.sum(RSD)

    for i in range(A):
        print(RD[i*A:i*A+A].tolist())
        print(RSD[i*A:i*A+A].tolist())
    RD = RD.tolist()
    RSD = RSD.tolist()
    print(JSD_core(RD, RSD))


if __name__ == '__main__':
    main()

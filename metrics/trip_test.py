"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : HZT
# @File    : trip_test.py
# @Software: PyCharm
-------------------------------------
"""

import os
from math import log

import numpy as np
from joblib import Parallel, delayed


def KLD(p, q):  # 计算KL散度
    p = p + np.spacing(1)
    q = q + np.spacing(1)
    # print(p/q)

    return sum([_p * log(_p / _q) for (_p, _q) in zip(p, q)])


def JSD_core(p, q):  # 计算JS散度（Jensen–Shannon divergence）

    M = [0.5 * (_p + _q) for _p, _q in zip(p, q)]

    # p = p + np.spacing(1)
    # q = q + np.spacing(1)

    return 0.5 * KLD(p, M) + 0.5 * KLD(q, M)


def main(epsilon):
    n_grid = 7
    min_latitude = 39.4
    min_longitude = 115.7
    len_latitude = 41.6 - 39.4
    len_longitude = 117.4 - 115.7
    wei = len_latitude / n_grid
    jing = len_longitude / n_grid
    A = n_grid ** 2

    RD = np.zeros(A * A)
    RSD = np.zeros(A * A)
    D = []
    SD = []
    path_all = []
    base_path_list = os.listdir('../data/Geolife Trajectories 1.3/Beijing/t_fullv2/')
    for path in base_path_list:
        file_object = open('../data/Geolife Trajectories 1.3/Beijing/t_fullv2/' + path, 'r')
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

            T0.append(w * n_grid + j)
        D.append(T0)
        # print(T0[0]*A+T0[-1])
        RD[T0[0] * A + T0[-1]] += 1
        # print(T0)
        file_object.close()

    path_all = []
    base_path_list = os.listdir("../data/Geolife Trajectories 1.3/sd/sd_final_Beijing_ep{}".format(epsilon))
    for path in base_path_list:
        file_object = open(r"../data/Geolife Trajectories 1.3/sd/sd_final_Beijing_ep{}/".format(epsilon) + path, 'r')
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
            if w * n_grid + j < A:
                T0.append(w * n_grid + j)
        if T0:
            SD.append(T0)
            try:
                RSD[T0[0] * A + T0[-1]] += 1
            except Exception as e:
                print(e)
                continue

            # print(T0)
        file_object.close()

    RD = RD / np.sum(RD)
    RSD = RSD / np.sum(RSD)

    RD = RD.tolist()
    RSD = RSD.tolist()
    print('epsilon: ', epsilon, 'trip error: ', JSD_core(RD, RSD))


if __name__ == '__main__':
    epsilon_list = [0.1, 0.5, 1.0, 2.0]
    Parallel(n_jobs=4)(delayed(main)(i) for i in epsilon_list)

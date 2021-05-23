"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  :
             nomalocaris
             Giyn
             HZT
# @File    : diameter_error.py
# @Software: PyCharm
-------------------------------------
"""

import os
from math import log

import numpy as np
from utils import ProgressBar


def KLD(p, q):     # 计算KL散度
    p += np.spacing(1)
    q += np.spacing(1)

    return sum([_p * log(_p/_q) for (_p, _q) in zip(p, q)])


def JSD_core(p, q):  # 计算JS散度（Jensen–Shannon divergence）
    M = [0.5 * (_p + _q) for _p, _q in zip(p, q)]

    return 0.5 * KLD(p, M) + 0.5 * KLD(q, M)


def D_len(d_path):
    D = []
    path_all = []
    base_path_list = os.listdir(d_path)
    for path in base_path_list:
        file_object = open(d_path + path, 'r')
        T0 = []
        path_all.append(path)
        for line in file_object.readlines():
            jw = line.strip().split(',')
            w = jw[0]
            w = float(w)
            j = jw[1].strip()
            j = float(j)
            T0.append((w, j))
        D.append(T0)
    D_maxlen_arr = []
    D_maxlen = 0
    d_len = len(D)
    p = ProgressBar(d_len, '计算D轨迹长度')
    for i in range(d_len):  # 多条轨迹
        p.update(i)
        T0 = D[i]
        T_maxlen = 0
        for i in range(len(T0)):
            for j in range(i, len(T0)):
                if i==j:
                    continue
                else:
                    now_len = ((T0[i][0] - T0[j][0])**2 + (T0[i][1] - T0[j][1])**2)**0.5
                    if now_len > D_maxlen:
                        D_maxlen = now_len
                    if now_len > T_maxlen:
                        T_maxlen = now_len
        D_maxlen_arr.append(T_maxlen)
    return D_maxlen, D_maxlen_arr


def _cal_diameter_e(D_maxlen, D_maxlen_arr, SD_maxlen, SD_maxlen_arr):
    # 存入epsilon数组
    ep_D = [0 for _ in range(20)]
    ep_SD = [0 for _ in range(20)]
    for item in D_maxlen_arr:
        num = int(item/(D_maxlen/20))
        if num < 20:
            ep_D[num] += 1
        else:
            ep_D[19] += 1

    for item in SD_maxlen_arr:
        num = int(item/(SD_maxlen/20))
        if num < 20:
            ep_SD[num] += 1
        else:
            ep_SD[19] += 1

    ep_D = np.array(ep_D, dtype='float32')
    ep_D /= np.sum(ep_D)
    ep_D = ep_D.tolist()
    ep_SD = np.array(ep_SD, dtype='float32')
    ep_SD /= np.sum(ep_SD)
    ep_SD = ep_SD.tolist()
    dia_e = JSD_core(ep_D, ep_SD)
    return dia_e


def cal_diameter_e(d_path, sd_path):
    """"""
    # dm, dm_arr = D_len(d_path)
    dm = 1.4979605451980367
    with open("dm_arr.txt", "r") as output:
        dm_arr = eval(output.read())
    sdm, sdm_arr = D_len(sd_path)
    return _cal_diameter_e(dm, dm_arr, sdm, sdm_arr)


def count_d_path(d_path):
    dm, dm_arr = D_len(d_path)
    print("dm:", dm)
    with open("dm_arr.txt", "w") as output:
        output.write(str(dm_arr))
    print(dm_arr)


if __name__ == '__main__':
    # print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
    #                                                                     "1.3/sd/sd_final_MDL1100_ep0.1/"))
    # print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
    #                                                                           "1.3/sd/sd_final_MDL1100_ep0.5/"))
    # print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
    #                                                                           "1.3/sd/sd_final_MDL1100_ep1.0/"))
    # print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
    #                                                                           "1.3/sd/sd_final_MDL1100_ep2.0/"))
    # print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
    #                                                                     "1.3/test/0/"))
    # print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
    #                                                                           "1.3/test/1/"))
    print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
                                                                              "1.3/test/2/"))
    print(cal_diameter_e("../../data/Geolife Trajectories 1.3/Trajectories/", "../../data/Geolife Trajectories "
                                                                              "1.3/test/3/"))
    # count_d_path("../../data/Geolife Trajectories 1.3/Trajectories7000/")
    # with open("dm_arr.txt", "r") as output:
    #     print(eval(output.read()))

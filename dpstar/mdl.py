"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris、Giyn、HZT
# @File    : mdl.py
# @Software: PyCharm
-------------------------------------
"""

import os

import numpy as np

from utils import vlen
from utils import ProgressBar
from utils import to_vec_add
from utils import to_vec_sub
from utils import to_vec_times
from utils import to_vec_dot


def lt(t_traj, start_ind, curr_ind):
    """

    cal L(T~)

    Args:
        t_traj   :
        start_ind:
        curr_ind :

    Returns:


    """
    vlength = vlen(t_traj[start_ind], t_traj[curr_ind])

    return np.log2(vlength) if vlength else np.spacing(1)


def cal_perpendicular(si, ei, sj, ej):
    """

    Args:
        si:
        ei:
        sj:
        ej:

    Returns:

    """
    sisj = to_vec_sub(sj, si)
    siei = to_vec_sub(ei, si)
    siej = to_vec_sub(ej, si)
    _base = to_vec_dot(siei, siei)
    if _base == 0:
        return np.spacing(1)
    u1 = to_vec_dot(sisj, siei) / _base
    u2 = to_vec_dot(siej, siei) / _base
    ps = to_vec_add(si, to_vec_times(u1, siei))
    pe = to_vec_add(si, to_vec_times(u2, siei))
    lp1 = vlen(ps, sj)
    lp2 = vlen(pe, ej)
    if lp1 + lp2 == 0:
        outD = 0
    else:
        outD = (lp1 ** 2 + lp2 ** 2) / (lp1 + lp2)

    return outD


def angular(si, ei, sj, ej):
    """

    cal angular distance

    Args:
        si:
        ei:
        sj:
        ej:

    Returns:

    """
    siei = to_vec_sub(ei, si)
    sjej = to_vec_sub(ej, sj)
    if siei[0] == sjej[0] and siei[1] == sjej[1]:
        return 0
    if to_vec_dot(siei, sjej) <= 0:  # 90°≤α≤180°
        outD = np.sqrt(to_vec_dot(sjej, sjej))
    else:
        cos0 = to_vec_dot(siei, sjej) / (np.sqrt(to_vec_dot(siei, siei)) * np.sqrt(to_vec_dot(sjej, sjej)))
        if 1 - cos0 ** 2 > 0:
            sin0 = np.sqrt(1 - cos0**2)
        else:
            sin0 = 0
        outD = np.sqrt(to_vec_dot(sjej, sjej)) * sin0

    return outD


def lttilde(t_traj, start_ind, curr_ind):
    """

    cal L(T|T~)

    Args:
        t_traj   :
        start_ind:
        curr_ind :

    Returns:

    """
    score1 = 0
    score2 = 0
    for j in range(start_ind, curr_ind):
        if t_traj[start_ind] == t_traj[j] and t_traj[curr_ind] == t_traj[j + 1]:
            continue
        # 更长的放前面
        if vlen(t_traj[start_ind], t_traj[curr_ind]) > vlen(t_traj[j], t_traj[j + 1]):
            presult = cal_perpendicular(t_traj[start_ind], t_traj[curr_ind], t_traj[j], t_traj[j + 1])
            aresult = angular(t_traj[start_ind], t_traj[curr_ind], t_traj[j], t_traj[j + 1])
        else:
            presult = cal_perpendicular(t_traj[j], t_traj[j + 1], t_traj[start_ind], t_traj[curr_ind])
            aresult = angular(t_traj[j], t_traj[j + 1], t_traj[start_ind], t_traj[curr_ind])
        score1 += presult
        score2 += aresult

    score1 = np.log2(score1) if score1 != 0 else 0
    score2 = np.log2(score2) if score2 != 0 else 0

    return score1 + score2


def Tmdl(t_traj):
    """计算得到的用代表点表示的轨迹

    generate func, see: Trajectory Clustering: A Partition-and-Group Framework

    Args:
        t_traj:

    Returns:

    """
    Tlen = len(t_traj)  # 原始的点数
    if Tlen == 0:
        return []

    CP = list()
    CP.append(t_traj[0])    # 存放初始轨迹点
    startIndex = 0      # 原点
    length = 1

    while startIndex + length < Tlen:
        currIndex = startIndex + length
        if lttilde(t_traj, startIndex, currIndex) > 0:
            CP.append(t_traj[currIndex - 1])
            startIndex = currIndex - 1
            length = 1
        else:
            length += 1
    CP.append(t_traj[-1])

    return CP


def mdl_main(min_latitude, min_longitude, init_path, preserve_path, rate):
    """

    main func

    Args:
        min_latitude :
        min_longitude:
        init_path    :
        preserve_path:
        rate         :

    Returns:

    """
    if not os.path.exists(preserve_path):
        os.makedirs(preserve_path)
    base_path_list = os.listdir(init_path)
    tot_len = len(base_path_list)           # 有14650个
    p = ProgressBar(tot_len, 'MDL轨迹简化')
    for i in range(tot_len):
        path = base_path_list[i]
        p.update(i)
        # 打开独个轨迹数据
        with open(init_path + path, 'r') as file_object:
            T = []
            for line in file_object.readlines():
                jw = line.strip().split(',')
                w = float(jw[0].strip())
                j = float(jw[1].strip())
                T.append(((w - min_latitude)*rate, (j - min_longitude)*rate))  # 对轨迹点做映射
            t_tilde = Tmdl(T)  # 生成的轨迹
            # 查看生成的轨迹的长度，并检查有无空集
            print("代表点的长度", len(t_tilde))
            if not len(t_tilde):
                print(init_path + path)
                print(T)
            with open(preserve_path + path.strip().split('.')[0] + '.txt', 'w') as f3:
                for item in t_tilde:
                    f3.writelines(str(item) + '\n')


def cheak(path='../data/QG Taxi/MDL/'):
    base_path_list = os.listdir(path)
    for i in range(len(base_path_list)):
        path_ = base_path_list[i]
        with open(path + path_, 'r') as file_object:
            if len(file_object.readlines()) == 0:
                print("空的：", path_)


def check_data():
    length_ = []
    base_path_list = os.listdir('../data/QG Taxi/MDL/')
    for path in base_path_list:
        file_object = open('../data/QG Taxi/MDL/' + path, 'r')
        length_.append(len(file_object.readlines()))
    print(length_)
    print(np.mean(length_))
    print(np.std(length_, ddof=1))


if __name__ == '__main__':
    mdl_main(22.8, 112.7,
             '../data/QG Taxi/Trajectories/',
             '../data/QG Taxi/MDL/', 1200)
    cheak()
    check_data()

"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris、Giyn、HZT
# @File    : __init__.py
# @Software: PyCharm
-------------------------------------
"""

import os
from math import log

import numpy as np

from utils import ProgressBar


def read_trajs_data(trajs_path: str) -> list:
    """

    extract trajectory data

    Args:
        trajs_path: trajectory file location

    Returns:
        D_: trajectory list

    """
    D_ = []
    trajs_file_list = os.listdir(trajs_path)

    for file in trajs_file_list:
        with open(trajs_path + file, 'r') as traj_file:
            d = []
            for line in traj_file.readlines():
                d.append(eval(line))

            D_.append(d)

    return D_


def kld(p, q):
    """

    calculate kl divergence

    Args:
        p: probability distributions p
        q: probability distributions q

    Returns:

    """
    p += np.spacing(1)
    q += np.spacing(1)

    return sum([_p * log(_p / _q) for (_p, _q) in zip(p, q)])


def jsd(p, q):
    """

    calculate Jensen–Shannon divergence

    Args:
        p: probability distributions p
        q: probability distributions q

    Returns:

    """
    M = [0.5 * (_p + _q) for _p, _q in zip(p, q)]

    return 0.5 * kld(p, M) + 0.5 * kld(q, M)


def extra_same_elem(list1: list, list2: list) -> list:
    """

    extract the same part between 2 lists

    Args:
        list1: list 1
        list2: list 2

    Returns:
        same part between 2 lists

    """
    set1 = set(list1)
    set2 = set(list2)
    same_elem = set1.intersection(set2)

    return list(same_elem)


def d_len(trajs_path: str) -> (int, list):
    """

    calculate the length of the trajectory

    Args:
        trajs_path: trajectory file location

    Returns:
        D_max_length     : maximum trajectory length
        D_max_length_list: maximum trajectory length list

    """
    D = []
    files_list = os.listdir(trajs_path)

    for path in files_list[:4]:
        with open(trajs_path + path, 'r') as file:
            T = []
            for line in file.readlines():
                point = tuple(map(float, line.strip().split(',')))
                T.append(point)
            D.append(T)

    D_max_length_list = []
    D_max_length = 0
    traj_len = len(D)
    p = ProgressBar(traj_len, 'Calculate length of d trajectory')
    for i in range(traj_len):
        p.update(i)
        T_ = D[i]
        T_max_len = 0
        for i in range(len(T_)):
            for j in range(i, len(T_)):
                if i == j:
                    continue
                else:
                    now_len = ((T_[i][0] - T_[j][0]) ** 2 + (T_[i][1] - T_[j][1]) ** 2) ** 0.5
                    if now_len > D_max_length:
                        D_max_length = now_len
                    if now_len > T_max_len:
                        T_max_len = now_len
        D_max_length_list.append(T_max_len)

    return D_max_length, D_max_length_list

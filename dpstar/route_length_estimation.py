"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 12:27:34
# @Author  : Giyn
# @Email   : giyn.jy@gmail.com
# @File    : route_length_estimation.py
# @Software: PyCharm
-------------------------------------
"""

import random

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils import ProgressBar


def exp_mechanism(score, m, epsilon, sensitivity):
    """

    指数机制，选出一个符合定义的下标

    Args:
        score      :
        m          :
        epsilon    :
        sensitivity:

    Returns:

    """
    exponents_list = [0 for _ in range(m)]
    summary = 0
    sum_exp = 0

    for i in range(m):
        expo = 0.5 * (score[i]) * epsilon / sensitivity
        exponents_list[i] = np.exp(expo)

        summary += exponents_list[i]
    exponents_list = np.array(exponents_list)
    exponents_list /= summary
    r = random.random()
    j = 0

    while True:
        sum_exp = sum_exp + exponents_list[j]
        if sum_exp > r:
            break
        j += 1

    return j


def route_length_estimate(trajectory, A, lo, hi, epsilon, sensitivity):
    """

    轨迹长度估计

    Args:

    Returns:

    """
    C = A * A
    L_matrix = [[] for _ in range(C)]  # L矩阵
    L_array = []

    for t in trajectory:
        lenT = len(t)
        if lenT > hi:
            continue
        if lenT < 2 or lo > lenT:
            continue

        row = t[0]
        col = t[-1]
        l_index = row * A + col  # 转一维坐标
        L_matrix[l_index].append(lenT)

    p = ProgressBar(C, '计算轨迹中值长度矩阵')
    for i in range(C):
        p.update(i)
        score_arr = []
        K = L_matrix[i].copy()  # 取一种头尾轨迹的所有轨迹长
        K.sort()  # 顺序排序
        if len(K) < 1:
            L_array.append(0)
            continue
        m_index = len(K) / 2  # 中值下标
        for j in range(len(K)):
            score_arr.append(-abs(j - m_index))  # 得分函数
        r_index = exp_mechanism(score_arr, len(K), epsilon, sensitivity)
        # print(K, '--->', K[r_index])
        L_array.append(K[r_index])

    return L_array


def route_length_estimate_main(A, epsilon, src_file, out_file):
    """

    主函数

    Args:

    Returns:

    """
    with open(src_file, 'r') as grid_trajectories_file:
        # 网格轨迹数据(list)
        T = [eval(grid_trajectory) for grid_trajectory in grid_trajectories_file.readlines()]
        maxT = max([len(i) for i in T])
        with open(out_file, 'w') as route_length_file:
            l_array = route_length_estimate(T, A, 0, 1.25 * maxT, epsilon, 1)
            len_modify_func = lambda x: x if x >= 2 else 2
            l_array = [len_modify_func(x) for x in l_array]
            l_mat = np.array(l_array).reshape((A, A))
            for arr in l_mat:
                for i in range(len(arr)):
                    if i < len(arr) - 1:
                        route_length_file.write(str(arr[i])+' ')
                    else:
                        route_length_file.write(str(arr[i]) + '\n')
    sns.heatmap(data=l_mat, square=True)
    plt.title('route length estimation (epsilon=%s)' % str(used_pair[0]))
    plt.show()

    return maxT


if __name__ == '__main__':
    ep_grid_pairs = ((0.1, 67), (0.5, 120), (1.0, 193), (2.0, 364))
    used_pair = ep_grid_pairs[0]
    route_length_estimate_main(used_pair[1], used_pair[0] * 2 / 9,
                               f'../data/Geolife Trajectories 1.3/middleware/grid_traj_MDL1100_ep{used_pair[0]}.txt',
                               f'../data/Geolife Trajectories 1.3/middleware/length_traj_MDL1100_ep{used_pair[0]}.txt')

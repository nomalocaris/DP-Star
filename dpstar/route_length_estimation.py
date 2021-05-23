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

import numpy as np

from utils import ProgressBar


def exp_mechanism(score, m: int, _epsilon: float, sensitivity: float) -> int:
    """

    指数机制，选出一个符合定义的下标

    Args:
        score      :
        m          :
        _epsilon   :
        sensitivity:

    Returns:
        j:

    """
    exponents_list = [0 for _ in range(m)]
    summary = 0
    sum_exp = 0

    for i in range(m):
        expo = 0.5 * (score[i]) * _epsilon / sensitivity
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


def route_length_estimate(trajs: list, n_grid: int, lo, hi: float, _epsilon: float,
                          sensitivity: float) -> list:
    """

    轨迹长度估计

    Args:
        trajs      :
        n_grid     :
        lo         :
        hi         :
        _epsilon   :
        sensitivity:

    Returns:
        L:

    """
    C = n_grid * n_grid
    L_matrix = [[] for _ in range(C)]  # L矩阵
    L = []

    for t in trajs:
        lenT = len(t)
        if lenT > hi:
            continue
        if lenT < 2 or lo > lenT:
            continue

        row = t[0]
        col = t[-1]
        l_index = row * n_grid + col  # 转一维坐标
        L_matrix[l_index].append(lenT)

    p = ProgressBar(C, '计算轨迹中值长度矩阵')
    for i in range(C):
        p.update(i)
        score_arr = []
        K = L_matrix[i].copy()  # 取一种头尾轨迹的所有轨迹长
        K.sort()  # 顺序排序
        if len(K) < 1:
            L.append(0)
            continue
        m_index = len(K) / 2  # 中值下标
        for j in range(len(K)):
            score_arr.append(-abs(j - m_index))  # 得分函数
        r_index = exp_mechanism(score_arr, len(K), _epsilon, sensitivity)
        # print(K, '--->', K[r_index])
        L.append(K[r_index])

    return L


def route_length_estimate_main(n_grid: int, _epsilon: float, grid_trajs_path: str,
                               routes_length_path: str) -> int:
    """

    主函数

    Args:
        n_grid            : 网格数
        _epsilon          : 隐私预算
        grid_trajs_path   : 网格轨迹文件路径
        routes_length_path: 轨迹长度估计文件路径

    Returns:
        maxT: 最大轨迹长度

    """
    with open(grid_trajs_path, 'r') as grid_trajs_file:
        # 网格轨迹数据(list)
        T = [eval(grid_traj) for grid_traj in grid_trajs_file.readlines()]
        maxT = max([len(i) for i in T])
        with open(routes_length_path, 'w') as routes_length_file:
            l_array = route_length_estimate(T, n_grid, 0, 1.25 * maxT, _epsilon, 1.0)
            len_modify_func = lambda x: x if x >= 2 else 2
            l_array = [len_modify_func(x) for x in l_array]
            l_mat = np.array(l_array).reshape((n_grid, n_grid))
            for arr in l_mat:
                for i in range(len(arr)):
                    if i < len(arr) - 1:
                        routes_length_file.write(str(arr[i]) + ' ')
                    else:
                        routes_length_file.write(str(arr[i]) + '\n')

    print('最大网格轨迹长度: %d' % maxT)

    return maxT


if __name__ == '__main__':
    epsilon = 0.1
    route_length_estimate_main(64, epsilon * 2 / 9,
                               f'../data/Geolife Trajectories 1.3/Middleware/grid_trajs_epsilon_{epsilon}.txt',
                               f'../data/Geolife Trajectories 1.3/Middleware/routes_length_epsilon_{epsilon}.txt')

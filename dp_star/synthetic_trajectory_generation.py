"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 12:28:08
# @Author  : Giyn
# @Email   : giyn.jy@gmail.com
# @File    : synthetic_trajectory_generation.py
# @Software: PyCharm
-------------------------------------
"""

import random

import numpy as np

from utils import ProgressBar


def synthetic_trajs(n_grid: int, max_t_len: int, trip_distribution_path: str,
                    midpoint_movement_path: str, routes_length_path: str, sd_path: str, nSyn: int):
    """

    综合轨迹生成

    Args:
        n_grid                : 网格数量
        max_t_len             : 最大网格轨迹长度
        trip_distribution_path: 起止点分布概率矩阵路径
        midpoint_movement_path: 马尔可夫转移概率矩阵路径
        routes_length_path    : 轨迹长度估计矩阵
        sd_path               : 综合生成轨迹路径
        nSyn                  : 轨迹条数

    Returns:

    """
    # 起止点分布概率矩阵
    with open(trip_distribution_path, 'r') as trip_distribution_file:
        R = np.array([list(map(lambda x: float(x), line.split(' '))) for line in trip_distribution_file.readlines()])

    # 马尔可夫转移概率矩阵
    with open(midpoint_movement_path, 'r') as midpoint_movement_file:
        X = np.array([list(map(lambda x: float(x), line.split(' '))) for line in midpoint_movement_file.readlines()])

    X_copy = X.copy()
    X_array = [X_copy]
    # 先对转移概率矩阵做乘方，迭代一定次数后基本不变
    for i in range(max_t_len):
        X_array.append(X_array[i] @ X_copy)

    X_array_len = len(X_array)

    # 轨迹长度估计矩阵
    with open(routes_length_path, 'r') as routes_length_file:
        L = [i for each in [list(map(lambda x: float(x), line.split(' '))) for line in routes_length_file.readlines()] for i in each]

    # 综合
    with open(sd_path, 'w') as sd_file:
        # line 1: Initialize SD as empty set
        SD = []
        index_list = [j for j in range(n_grid * n_grid)]
        R /= np.sum(R)

        p = ProgressBar(nSyn, '生成网格化的脱敏数据')
        # line 2-6
        for i in range(nSyn):
            p.update(i)
            # Pick a sample S = (C_start, C_end) from Rˆ
            index = np.random.choice(index_list, p=R.ravel())

            start_point = int(index / n_grid)  # 网格轨迹起点
            end_point = index - start_point * n_grid  # 网格轨迹终点

            l_hat = L[index]  # 轨迹长度参数

            s = int(np.round(random.expovariate(np.log(2) / l_hat)))  # 指数分布取轨迹长
            if s < 2:
                s = 2

            T = []
            prev_point = start_point
            T.append(prev_point)  # 加入起始点

            # line 7-10
            for j in range(1, s-1):
                # 论文公式，X的s-j倍，寻找X_array下标，超过X_array长度则取最后一个
                if s - 1 - j - 1 >= X_array_len:
                    X_now = X_array[-1]
                else:
                    X_now = X_array[s - 1 - j - 1]
                # Sample
                sample_prob = []
                for k in range(n_grid):
                    sample_prob.append(X_now[k][end_point] * X[prev_point][k])  # 加入取样概率

                sample_prob = np.array(sample_prob)
                if np.sum(sample_prob) == 0:
                    continue
                sample_prob /= np.sum(sample_prob)  # 归一化
                now_point = np.random.choice([int(m) for m in range(n_grid)],
                                             p=sample_prob.ravel())  # 抽样
                prev_point = now_point  # 更新上一个点
                T.append(now_point)  # 加入轨迹中

            T.append(end_point)  # 加入结束点
            SD.append(T)  # 加入轨迹

        for sd in SD:
            sd_file.writelines(str(sd) + '\n')


if __name__ == '__main__':
    epsilon = 0.1
    synthetic_trajs(64, 235,
                    f'../data/Geolife Trajectories 1.3/Middleware/trip_distribution_epsilon_{epsilon}.txt',
                    f'../data/Geolife Trajectories 1.3/Middleware/midpoint_movement_epsilon_{epsilon}.txt',
                    f'../data/Geolife Trajectories 1.3/Middleware/routes_length_epsilon_{epsilon}.txt',
                    f'../data/Geolife Trajectories 1.3/SD/sd_epsilon_{epsilon}.txt',
                    14650)

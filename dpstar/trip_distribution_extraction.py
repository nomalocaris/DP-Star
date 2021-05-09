"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 11:57:44
# @Author  : Giyn
# @Email   : giyn.jy@gmail.com
# @File    : trip_distribution_extraction.py
# @Software: PyCharm
-------------------------------------
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from config import *
from utils import ProgressBar


def trip_distribution(trajectory, N, epsilon) -> np.ndarray:
    """

    获取转移概率矩阵

    Args:
        trajectory: 轨迹数据(二维数组)
        N         : 二级网格数
        epsilon   : 隐私预算

    Returns:
        R: 转移概率矩阵

    """
    R = np.zeros((N, N))  # 建立 N*N 的转移概率矩阵
    for t in trajectory:
        if len(t) > 1:
            sta = t[0]
            end = t[-1]
            R[sta][end] += 1

    count = int(np.sum(R))  # 轨迹条数

    p = ProgressBar(N, '生成转移概率矩阵')
    for i in range(N):
        p.update(i)
        for j in range(N):
            noise = np.random.laplace(0, 1 / epsilon)  # 添加拉普拉斯噪声
            R[i][j] += noise

            if R[i][j] < 0:
                R[i][j] = 0

    R /= count

    # 绘制转移概率矩阵热力图
    sns.heatmap(data=R, square=True)
    plt.title('trip distribution (epsilon=%s)' % str(used_pair[0]))
    plt.show()

    return R


def trip_distribution_main(A, epsilon, src_file, out_file):
    """

    主函数(将转移概率矩阵写入文件)

    Args:
        A       : 网格数
        epsilon : 隐私预算
        src_file: 网格轨迹文件路径
        out_file: 转移概率矩阵输出文件路径

    Returns:

    """
    with open(src_file, 'r') as grid_trajectories_file:
        # 网格轨迹数据(list)
        T = [eval(grid_trajectory) for grid_trajectory in grid_trajectories_file.readlines()]
        with open(out_file, 'w') as trip_distribution_file:
            trip_distribution_matrix = trip_distribution(T, A, epsilon)
            for item in trip_distribution_matrix:
                each_line = ' '.join([str(i) for i in item]) + '\n'
                trip_distribution_file.writelines(each_line)


if __name__ == '__main__':
    ep_grid_pairs = ((0.1, 67), (0.5, 120), (1.0, 193), (2.0, 364))
    used_pair = ep_grid_pairs[0]
    trip_distribution_main(used_pair[1], used_pair[0] * 1 / 9,
                           f'../data/Geolife Trajectories 1.3/middleware/grid_traj_MDL1100_ep{used_pair[0]}.txt',
                           f'../data/Geolife Trajectories 1.3/middleware/trip_distribution_MDL1100_ep{used_pair[0]}.txt')

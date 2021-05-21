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

import numpy as np

from utils import ProgressBar


def trip_distribution(trajs: list, n_grid: int, _epsilon: float) -> np.ndarray:
    """

    获取转移概率矩阵

    Args:
        trajs  : 轨迹数据(二维数组)
        n_grid : 二级网格数
        _epsilon: 隐私预算

    Returns:
        R: 转移概率矩阵

    """
    R = np.zeros((n_grid, n_grid))  # 建立 n_grid * n_grid 的转移概率矩阵
    for t in trajs:
        if len(t) > 1:
            sta = t[0]
            end = t[-1]
            R[sta][end] += 1

    count = int(np.sum(R))  # 轨迹条数

    p = ProgressBar(n_grid, '生成转移概率矩阵')
    for i in range(n_grid):
        p.update(i)
        for j in range(n_grid):
            noise = np.random.laplace(0, 1 / _epsilon)  # 添加拉普拉斯噪声
            R[i][j] += noise

            if R[i][j] < 0:
                R[i][j] = 0

    R /= count

    return R


def trip_distribution_main(n_grid: int, _epsilon: float, grid_trajs_path: str,
                           trip_distribution_path: str):
    """

    主函数(将转移概率矩阵写入文件)

    Args:
        n_grid                : 网格数
        _epsilon              : 隐私预算
        grid_trajs_path       : 网格轨迹文件路径
        trip_distribution_path: 转移概率矩阵输出文件路径

    Returns:

    """
    with open(grid_trajs_path, 'r') as grid_trajs_file:
        # 网格轨迹数据(list)
        T = [eval(grid_traj) for grid_traj in grid_trajs_file.readlines()]
        with open(trip_distribution_path, 'w') as trip_distribution_file:
            trip_distribution_matrix = trip_distribution(T, n_grid, epsilon)
            for item in trip_distribution_matrix:
                each_line = ' '.join([str(i) for i in item]) + '\n'
                trip_distribution_file.writelines(each_line)


if __name__ == '__main__':
    epsilon = 0.1
    trip_distribution_main(64, 0.1 * 3 / 9,
                           f'../data/Geolife Trajectories 1.3/Middleware/grid_trajs_epsilon_{epsilon}.txt',
                           f'../data/Geolife Trajectories 1.3/Middleware/trip_distribution_epsilon_{epsilon}.txt')

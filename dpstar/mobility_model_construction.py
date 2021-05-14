"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 12:03:46
# @Author  : Giyn
# @Email   : giyn.jy@gmail.com
# @File    : mobility_model_construction.py
# @Software: PyCharm
-------------------------------------
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils import ProgressBar


def markov_model(trajectory, N, epsilon):
    """

    马尔可夫模型

    Args:
        trajectory: 轨迹数据(二维数组)
        N         : 二级网格数
        epsilon   : 隐私预算

    Returns:
        O_: 中间点转移概率矩阵

    """
    O_ = np.zeros((N, N))  # 建立 N*N 的转移概率矩阵
    for t in trajectory:
        O_sub = np.zeros((N, N))
        for i in range(len(t) - 1):
            curr_point = t[i]
            next_point = t[i + 1]
            O_sub[curr_point][next_point] += 1
        O_sub /= (len(t) - 1)  # 该轨迹的转移概率
        O_ += O_sub

    p = ProgressBar(N, '生成中间点转移概率矩阵')
    for i in range(N):
        p.update(i)
        for j in range(N):
            noise = np.random.laplace(0, 1 / epsilon)  # 添加拉普拉斯噪声
            O_[i][j] += noise

            if O_[i][j] < 0:
                O_[i][j] = 0

    # compute X
    row_sum = [sum(O_[i]) for i in range(N)]
    for j in range(N):
        O_[j] /= row_sum[j]

    # 绘制矩阵热力图
    sns.heatmap(data=O_, square=True)
    plt.title('mobility model construction matrix (epsilon=%s)' % str(used_pair[0]))
    plt.show()

    return O_


def mobility_model_main(A, epsilon, src_file, out_file):
    """

    主函数

    Args:
        A       : 网格数
        epsilon : 隐私预算
        src_file: 网格轨迹文件路径
        out_file: 中间点转移概率矩阵文件路径
    Returns:

    """
    with open(src_file, 'r') as trajectory_file:
        T = [eval(trajectory) for trajectory in trajectory_file.readlines()]  # 网格轨迹数据(list)
        with open(out_file, 'w') as midpoint_movement_file:
            midpoint_movement_matrix = markov_model(T, A, epsilon)
            for item in midpoint_movement_matrix:
                each_line = ' '.join([str(i) for i in item]) + '\n'
                midpoint_movement_file.writelines(each_line)


if __name__ == '__main__':
    ep_grid_pairs = ((0.1, 67), (0.5, 120), (1.0, 193), (2.0, 364))
    used_pair = ep_grid_pairs[0]
    mobility_model_main(used_pair[1], used_pair[0] * 1 / 9,
                        f'../data/Geolife Trajectories 1.3/middleware/grid_traj_MDL1100_ep{used_pair[0]}.txt',
                        f'../data/Geolife Trajectories 1.3/middleware/midpoint_movement_MDL1100_ep{used_pair[0]}.txt')

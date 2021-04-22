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

import math
import random

import numpy as np

from config import *
from utils import signum, ProgressBar


def markov_model(trajectory, N, epsilon):
    """basic description

    detailed description

    Args:
        trajectory: 轨迹数据(二维数组)
        N         : 二级网格数
        epsilon   : 隐私预算

    Returns:
        O_: 中间点转移概率矩阵

    """
    O_ = np.zeros([N, N])  # 建立N*N的转移概率矩阵
    for t in trajectory:
        O_0 = np.zeros([N, N])
        for i in range(len(t) - 1):
            curr_point = t[i]
            next_point = t[i + 1]
            O_0[curr_point][next_point] += 1
        O_0 = O_0 / (len(t) - 1)  # 该轨迹的转移概率
        O_ += O_0

    line_all = []
    p = ProgressBar(N, '建立中间点转移概率矩阵')
    for i in range(N):
        p.update(i)
        score = 0
        for j in range(N):
            # 添加噪声
            sensitivity = 1
            randomDouble = random.random() - 0.5
            noise = - (sensitivity / epsilon) * signum(randomDouble) * math.log(
                1 - 2 * abs(randomDouble))

            O_[i][j] += noise
            if O_[i][j] < 0:
                O_[i][j] = 0
            score += O_[i][j]
        line_all.append(score)

    # compute X，归一
    for i in range(N):
        O_[i] /= line_all[i]

    return O_


def mobility_model_main(A, epsilon, trip_file=opath_grid_traj, out_file=x_path):
    """

    主函数

    Args:

    Returns:

    """
    with open(trip_file, 'r') as file_object:
        T_all = []
        for line in file_object.readlines():
            T = []
            line = line.strip()[1:-1]
            line_array = line.split(',')
            for step in line_array:
                if len(step.strip()):
                    T.append(int(step.strip()))
            T_all.append(T)

        with open(out_file, 'w') as fm:
            for row in markov_model(T_all, A, epsilon):
                out_line = ''
                for i in row.tolist():
                    out_line += ' ' + str(i)

                out_line += '\n'
                fm.writelines(out_line)

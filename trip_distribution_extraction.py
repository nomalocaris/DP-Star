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

import math
import random

import numpy as np

from utils import ProgressBar
from utils import signum


def trip_distribution(trajectory, N, epsilon):
    """

    获取行程分布

    Args:
        trajectory: 轨迹数据(二维数组)
        N         : 二级网格数
        epsilon   : 隐私预算

    Returns:
        R: 转移概率矩阵

    """
    R = np.zeros((N, N))  # 每个格子建立转移概率矩阵
    for t in trajectory:
        if len(t) > 1:
            sta = t[0]
            end = t[-1]
            R[sta][end] += 1

    count = 0

    p = ProgressBar(N, '建立转移概率矩阵')
    for i in range(N):
        p.update(i)
        for j in range(N):
            # 添加拉普拉斯噪声
            sensitivity = 1
            randomDouble = random.random() - 0.5
            noise = - (sensitivity / epsilon) * signum(randomDouble) * math.log(
                1 - 2 * abs(randomDouble))

            R[i][j] += noise

            if R[i][j] < 0:
                R[i][j] = 0

            count += R[i][j]
    R /= count

    return R


def main(trip_file, out_file, a, epsilon):
    """

    主函数

    Args:
        trip_file:
        out_file:
        a:
        epsilon:

    Returns:

    """
    with open(trip_file, 'r') as file_object:
        T_all = []
        for line in file_object.readlines():
            T = []
            line = line.strip()[1:-1]
            line_array = line.split(',')
            print(line_array)
            for step in line_array:
                if len(step.strip()):
                    T.append(int(step.strip()))
            T_all.append(T)

        with open(out_file, 'w') as f_trip:
            count = 0
            for item in trip_distribution(T_all, a, epsilon):
                line_str = ''
                for item2 in item:
                    line_str += str(item2) + ' '
                    count += item2
                line_str += '\n'
                f_trip.writelines(line_str)


if __name__ == '__main__':
    main('data/Geolife Trajectories 1.3/middleware/grid_traj.txt', 'data/Geolife Trajectories 1.3/middleware/trip_distribution.txt', 18, 6 / 9)

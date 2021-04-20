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


def exp_mechanism(score, m, epsilon, sensitivity):
    """

    指数机制，选出一个符合定义的下标

    Args:
        score:
        m:
        epsilon:
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
    """basic description

    detailed description

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
        L_array.append(K[r_index])

    return L_array


def main(trip_file, out_file, A, epsilon):
    """

    主函数

    Args:

    Returns:

    """
    with open(trip_file, 'r') as file_object:
        with open(out_file, 'w') as f_out:
            T_all = []
            maxT = 0
            for line in file_object.readlines():
                T = []
                line = line.strip()[1:-1]
                line_array = line.split(',')
                for step in line_array:
                    if len(step.strip()) > 0:
                        T.append(int(step.strip()))
                if len(T) > maxT:
                    maxT = len(T)
                T_all.append(T)
            count = 0
            star = ''
            for i in route_length_estimate(T_all, A, 0, 1.25 * maxT, epsilon, 1):
                if i < 2:
                    i = 2
                star += str(i) + ' '
                count += 1

                if count % A == 0:
                    star += '\n'
                    f_out.writelines(star)
                    star = ''

    print(maxT)

    return maxT


if __name__ == '__main__':
    main('../data/Geolife Trajectories 1.3/middleware/grid_traj.txt',
         'data/Geolife Trajectories 1.3/middleware/length_traj_Giyn.txt', 1012, 3 / 9)

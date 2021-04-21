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

from config import *
from utils import ProgressBar


def syn(aa_path=opath_grid_traj, omega_path=omega_path, r_path=r_path, x_path=x_path,
        l_path=l_path, sd_path=sd_path, sd_final_path=sd_final_path, max_t_len=94,
        min_latitude=0, min_longitude=0, A=1012, nSyn=14650):
    """basic description

    detailed description

    Args:

    Returns:

    """
    # 输入自适应网格A, trip分布矩阵R，转移矩阵X，中位数长度L，生成轨迹数量nSyn
    with open(aa_path) as f:
        AA = list()
        for line in f.readlines():
            AA += eval(line)
    with open(omega_path) as f:
        M_omega = list()
        for line in f.readlines():
            M_omega += eval(line)

    # 读trip分布矩阵
    r_file = open(r_path, 'r')
    R = []
    for row in r_file.readlines():
        row = row.strip()
        R_ele = []
        for ele in row.split(' '):
            R_ele.append(float(ele))

        R.append(R_ele)
    # 读马尔科夫转移概率矩阵
    x_file = open(x_path, 'r')
    X = []

    for row in x_file.readlines():
        row = row.strip()
        X_ele = []
        count = 0
        for ele in row.split(' '):
            X_ele.append(float(ele))
            count += float(ele)
        X.append(X_ele)

    X_np = np.array(X)

    X_copy = X_np.copy()
    X_array = [X_copy]
    # 先对转移概率矩阵做乘方，迭代一定次数后基本不变
    for i in range(max_t_len):
        X_array.append(X_array[i].dot(X_copy))

    X_array_len = len(X_array)
    # 读轨迹长度矩阵
    l_file = open(l_path, 'r')
    L = []
    for row in l_file.readlines():
        row = row.strip()
        for ele in row.split(' '):
            L.append(float(ele))

    sd_file = open(sd_path, 'w')
    sd_final_file = open(sd_final_path, 'w')

    # 开始综合
    # line 1: Initialize SD as empty set
    SD = []
    p1 = ProgressBar(nSyn, '生成脱敏数据')
    for i in range(nSyn):
        p1.update(i)
        # Pick a sample S = (Cstart, Cend) from Rˆ
        index_array = [int(j) for j in range(A * A)]
        R = np.array(R)
        R = R / np.sum(R)
        # 选trip 分布
        index = np.random.choice(index_array, p=R.ravel())

        start_point = int(index / A)  # 轨迹起点
        end_point = index - start_point * A  # 轨迹终点

        l_now = L[index]  # 轨迹长度参数
        r_length = random.expovariate(np.log(2) / l_now)  # 指数分布取轨迹长
        r_length = int(np.round(r_length))  # 整数化
        if r_length < 2:
            r_length = 2
        T = []
        prev_point = start_point
        T.append(prev_point)  # 加入起始点
        # line 7-10
        for j in range(1, r_length - 1):
            # 论文公式，X的r_length-j倍，寻找X_array下标，超过X_array长度则取最后一个
            if r_length - 1 - j - 1 >= X_array_len:
                X_now = X_array[-1]
            else:
                X_now = X_array[r_length - 1 - j - 1]
            # Sample
            sample_prob = []
            for k in range(A):
                sample_prob.append(X_now[k][end_point] * X_np[prev_point][k])  # 加入取样概率

            sample_prob = np.array(sample_prob)
            if np.sum(sample_prob) == 0:
                continue
            sample_prob = sample_prob / np.sum(sample_prob)  # 归一化
            now_point = np.random.choice([int(m) for m in range(A)], p=sample_prob.ravel())  # 抽样
            prev_point = now_point  # 更新上一个点
            T.append(now_point)  # 加入轨迹中

        T.append(end_point)  # 加入结束点
        SD.append(T)  # 加入轨迹

    for sd in SD:
        sd_file.writelines(str(sd) + '\n')
    sd_file.close()

    # 转化成原数据坐标
    SD_final = []
    p2 = ProgressBar(nSyn, '脱敏数据坐标转换并写入文件')
    for i in range(nSyn):
        p2.update(i)
        T = SD[i]
        T_final = []
        for j in range(len(T)):
            # 确定M与A位置
            C_index = T[j]
            a_count = 0
            for k in range(A):
                A_a = AA[k]
                a_count += A_a * A_a
                if a_count > C_index:
                    # M位置
                    m_index = k
                    m_start = M_omega[m_index][0]  # 大格子范围坐标
                    m_end = M_omega[m_index][1]

                    row_base = (m_end[0] - m_start[0]) / A_a
                    col_base = (m_end[1] - m_start[1]) / A_a

                    rela_A = C_index - (a_count - A_a * A_a)  # 相对位置
                    row = int(rela_A / A_a)
                    col = rela_A - row * A_a

                    start_point = (row * row_base, col * col_base)
                    end_point = ((row + 1) * row_base, (col + 1) * col_base)

                    # 随机取样
                    res_row = random.uniform(start_point[0], end_point[0])
                    res_col = random.uniform(start_point[1], end_point[1])

                    out_point = (
                        (res_row + m_start[0]) / 300 + min_latitude,
                        (res_col + m_start[1]) / 300 + min_longitude)
                    T_final.append(out_point)
                    break
        SD_final.append(T_final)

    # 写入文件
    for sd in SD_final:
        sd_final_file.writelines(str(sd) + '\n')
    sd_final_file.close()


if __name__ == '__main__':
    syn()

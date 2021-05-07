# -*- encoding:utf-8 -*-
import numpy as np
import random
import os
import datetime

count_get = 0
path_list = ['../../data/Geolife Trajectories 1.3/Trajectories7000/', '../../data/Geolife Trajectories '
                                                                      '1.3/sd/sd_final_MDL1100_ep0.1/',
             '../../data/Geolife '
             'Trajectories '
             '1.3/sd/sd_final_MDL1100_ep0.5/',
             '../../data/Geolife Trajectories 1.3/sd/sd_final_MDL1100_ep1.0/', '../../data/Geolife Trajectories '
                                                                               '1.3/sd/sd_final_MDL1100_ep2.0/']
path_test = ['../../data/Geolife Trajectories 1.3/Trajectories/', '../../data/Geolife Trajectories '
                                                                  '1.3/test/0/', '../../data/Geolife '
                                                                                 'Trajectories '
                                                                                 '1.3/test/1/',
             '../../data/Geolife Trajectories 1.3/test/2/', '../../data/Geolife Trajectories '
                                                            '1.3/test/3/']


# 参数：范围起点，范围终点，半径，查询数量，
def query(start_point, end_point, radius, D, SD):
    point_row = random.uniform(start_point[0], end_point[0])
    point_col = random.uniform(start_point[1], end_point[1])
    count_d = 0
    count_sd = 0
    b = int(len(D) * 0.01)
    for i in range(len(D)):
        for step in D[i]:
            if (step[0] - point_row) ** 2 + (step[1] - point_col) ** 2 <= radius ** 2:
                count_d += 1
                break
        for step in SD[i]:
            if (step[0] - point_row) ** 2 + (step[1] - point_col) ** 2 <= radius ** 2:
                count_sd += 1
                break
    if (count_d == 0 or count_sd == 0) and not (count_d == 0 and count_sd == 0) and not (
            count_d == 0 and count_sd < 10) and not (count_sd == 0 and count_d < 10):
        global count_get
        count_get += 1
    RE = abs(count_d - count_sd) / max(count_d, b)
    return RE


def get_data(init_path='../data/Geolife Trajectories 1.3/Trajectories/'):
    """
    提取出轨迹数据
    :param init_path:轨迹存储位置
    :return:轨迹列表
    """
    D = []
    base_path_list = os.listdir(init_path)
    for path in base_path_list:
        file_object = open(init_path + path, 'r')
        T0 = []
        for line in file_object.readlines():
            w = float(line.strip().split(',')[0].strip())
            j = float(line.strip().split(',')[1].strip())
            T0.append((w, j))
        D.append(T0)
    return D


def get_QA(D, SD, min_latitude=39.6,
           min_longitude=115.8,
           len_latitude=1.2,
           len_longitude=1.6):
    """
    计算QA指标
    :param D:原始数据
    :param SD:生成数据
    :param min_latitude:纬度下界
    :param min_longitude:经度下界
    :param len_latitude:纬度上界
    :param len_longitude:经度下界
    :return:QA
    """

    error_r = 0
    for it in range(10):  # 多次算均值
        error_r += query((min_latitude, min_longitude), (min_latitude + len_latitude, min_longitude + len_longitude),
                         0.01, D, SD)
    return error_r / 10


if __name__ == '__main__':
    D = get_data(path_list[0])
    # with open("QAD.txt", "r") as output:
    #     D = eval(output.read())
    # print(D)
    for i in range(1, len(path_test)):
        if i == 1 or i == len(path_test) - 1:
            SD = get_data(path_test[i])
            RE = get_QA(D, SD)
            print(path_test[i], RE)

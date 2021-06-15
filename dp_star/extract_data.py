"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris、Giyn、HZT
# @File    : extract_data.py
# @Software: PyCharm
-------------------------------------
"""

import os
import random

import numpy as np

from utils import ProgressBar
from utils import cal_time_interval


def extract_dataset(lat_lon, trajs_name_file, init_path, base_path, rand_num):
    """

    对数据进行抽取

    Args:
        lat_lon        : 经纬度的界限值
        trajs_name_file: 用于存储Trajectory里面的文件名
        init_path      : 抽取后数据的存储路径
        base_path      : 原始数据
        rand_num       : 所有数据的数量

    Returns:

    """
    if not os.path.exists(init_path):
        os.makedirs(init_path)
    D = []
    file_list = []
    traj_fs = os.listdir(base_path)
    p1 = ProgressBar(len(traj_fs), '提取轨迹')

    for t in range(len(traj_fs)):  # 0-181名用户的轨迹数据
        p1.update(t)
        base_name = traj_fs[t]
        file_path = base_path + "/" + base_name + '/Trajectory/'
        files = os.listdir(file_path)  # 打开文件夹
        for f in files:  # 遍历文件
            line_count = 0  # 轨迹段计数
            with open(file_path + f) as fr:
                T = []
                prev_time = 0
                lines = fr.readlines()
                for id in range(6, len(lines)):
                    now_line = lines[id].strip().split(',')
                    now_line_latitude = float(now_line[0])
                    now_line_longitude = float(now_line[1])
                    # 检验是否在划定范围内
                    if lat_lon[0] < now_line_latitude < lat_lon[1] \
                            and lat_lon[2] < now_line_longitude < lat_lon[3]:
                        now_line_time = now_line[6]
                        line_count += 1
                        if line_count > 1:
                            now_time = now_line_time
                            t_interval = cal_time_interval(prev_time, now_time)
                            if t_interval > 6500:
                                # 轨迹间隔超过一定范围, 退出读取
                                break
                        prev_time = now_line_time
                        T.append((now_line_latitude, now_line_longitude))
                    else:
                        # 经纬度超过范围
                        if line_count:
                            break
                        else:
                            continue
                if line_count < 3:
                    # 轨迹长度小于3，跳过
                    continue
                D.append(T)
                file_list.append(base_name + '_' + f)

    rand_ind = random.sample([i for i in range(len(file_list))], rand_num)  # 随机抽取轨迹
    with open(trajs_name_file, 'w') as f2:
        p2 = ProgressBar(rand_num, '写入文件')
        for i in range(rand_num):
            p2.update(i)
            f2.writelines(file_list[rand_ind[i]] + '\n')
            with open(init_path + file_list[rand_ind[i]], 'w') as f3:
                for step in D[rand_ind[i]]:
                    f3.writelines(str(step[0]) + ',' + str(step[1]) + '\n')


def euclidean_distance(m, n):
    """

    计算欧式距离

    Args:

        m: 数据1
        n: 数据2

    Returns:

    """
    return np.sqrt((m-n)[0]**2 + (m-n)[1]**2)


def check_data():
    """

    检查数据

    Args:

    Returns:

    """
    length_ = []
    base_path_list = os.listdir('../data/Geolife Trajectories 1.3/Trajectories/')
    for path in base_path_list:
        with open('../data/Geolife Trajectories 1.3/Trajectories/' + path, 'r') as file_object:
            length_.append(len(file_object.readlines()))
    print(length_)
    print(np.mean(length_))
    print(np.std(length_, ddof=1))


if __name__ == '__main__':
    extract_dataset([39.4, 41.6, 115.7, 117.4],
                    '../data/Geolife Trajectories 1.3/trajs_name_file.txt',
                    '../data/Geolife Trajectories 1.3/Trajectories/',
                    '../data/Geolife Trajectories 1.3/Data', 14650)
    check_data()

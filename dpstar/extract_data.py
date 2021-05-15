#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""Geolife 轨迹提取相关函数"""
import random
import os
from utils import cal_time_interval
from utils import ProgressBar
import numpy as np
from joblib import Parallel, delayed


def extract_dataset(lat_lon, traj_fs, base_path, pid=0):
    """
    对数据进行抽取
    :param lat_lon:经纬度的界限值
    :param good_traj_file:用于存储Trajectory里面的文件名
    :param init_path:抽取后数据的存储路径
    :param base_path:原始数据
    :param rand_num:所有数据的数量,14650
    :return:
    """
    file_list = []
    D = []
    cnt = 0
    # p1 = ProgressBar(len(traj_fs), '提取轨迹')
    for t in range(len(traj_fs)):  # 对应名用户的轨迹数据
        # p1.update(t)
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
                if len(T) > 15:
                    # 轨迹长度必须大于一定数值
                    D.append(T)
                    file_list.append(base_name + '_' + f)
                    cnt += 1
                    if cnt % 100 == 0:
                        print('pid: %d traj num: %d' % (pid, cnt))
    return D, file_list


def write2files(init_path, file_list, D, write_file_num=14650):
    """写入文件
    """
    rand_ind = random.sample([i for i in range(len(file_list))], write_file_num)  # 随机抽取轨迹
    p2 = ProgressBar(write_file_num, '写入文件')
    for i in range(write_file_num):
        p2.update(i)
        with open(init_path + file_list[rand_ind[i]], 'w') as f2:
            for step in D[rand_ind[i]]:
                f2.writelines(str(step[0]) + ',' + str(step[1]) + '\n')


def EDistant(m, n):
    """
    计算欧式距离
    :param m:数据1
    :param n:数据2
    :return:
    """
    return np.sqrt((m-n)[0]**2 + (m-n)[1]**2)


def check_data(check_path):
    """检查是否符合要求
    """
    length_ = []
    base_path_list = os.listdir(check_path)
    for path in base_path_list:
        file_object = open(check_path + path, 'r')
        length_.append(len(file_object.readlines()))
    print(length_[:20])
    print(np.mean(length_))
    print(np.std(length_, ddof=1))


if __name__ == '__main__':
    from itertools import chain
    # [39.4, 41.6, 115.7, 117.4] 总的轮廓 t_fullv2 953.054 1761.367
    # [39.7, 40.2, 116.0, 116.8] 最密集的地方 t_densev1 903.496 1658.663
    # [39.7, 41.6, 115.7, 117.4] 最密集往左 t_leftv2 943.022 1789.898
    # [39.4, 40.2, 115.7, 117.4] 最密集往右 t_rightv1 910.620 1623.375
    # [39.4, 41.6, 116.0, 117.4] 最密集往上 t_upv1 951.595 1718.188
    # [39.4, 41.6, 115.7, 116.8] 最密集往下 t_downv1 937.325 1704.389
    base_path = 'H:/code/py/DP-Star/data/Geolife Trajectories 1.3/Data'
    new_path = 'H:/code/py/DP-Star/data/Geolife Trajectories 1.3/t_downv1/'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    traj_fs = os.listdir(base_path)
    n_worker = 5  # 进程数
    Ds, file_lists = zip(*Parallel(n_jobs=n_worker)(delayed(extract_dataset)
                                                    ([39.4, 41.6, 115.7, 116.8], fs, base_path, pid)
                                                    for fs, pid in zip(np.array_split(traj_fs, n_worker),
                                                                       range(n_worker))))
    D = list(chain(*Ds))
    file_list = list(chain(*file_lists))

    print('提取的轨迹数量: ', len(file_list))
    # extract_dataset([39.4, 41.6, 115.7, 117.4],
    #                 'H:/code/py/DP-Star/data/Geolife Trajectories 1.3/t_full/',
    #                 base_path)
    write2files(new_path, file_list, D)
    check_data(new_path)

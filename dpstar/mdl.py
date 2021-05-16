#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
import numpy as np
import os
from utils import vlen, ProgressBar, to_vec_add, to_vec_sub, to_vec_times, to_vec_dot
from joblib import Parallel, delayed


def lt(t_traj, start_ind, curr_ind):
    """cal L(T~)
    :param t_traj:
    :param start_ind:
    :param curr_ind:
    :return:
    """
    vlength = vlen(t_traj[start_ind], t_traj[curr_ind])
    return np.log2(vlength) if vlength else np.spacing(1)


def cal_perpendicular(si, ei, sj, ej):
    """
    :param si:
    :param ei:
    :param sj:
    :param ej:
    :return:
    """
    sisj = to_vec_sub(sj, si)
    siei = to_vec_sub(ei, si)
    siej = to_vec_sub(ej, si)
    _base = to_vec_dot(siei, siei)
    if _base == 0:
        return np.spacing(1)
    u1 = to_vec_dot(sisj, siei) / _base
    u2 = to_vec_dot(siej, siei) / _base
    ps = to_vec_add(si, to_vec_times(u1, siei))
    pe = to_vec_add(si, to_vec_times(u2, siei))
    lp1 = vlen(ps, sj)
    lp2 = vlen(pe, ej)
    if lp1 + lp2 == 0:
        outD = 0
    else:
        outD = (lp1 ** 2 + lp2 ** 2) / (lp1 + lp2)
    return outD


def angular(si, ei, sj, ej):
    """cal angular distance
    :param si:
    :param ei:
    :param sj:
    :param ej:
    :return:
    """
    siei = to_vec_sub(ei, si)
    sjej = to_vec_sub(ej, sj)
    if siei[0] == sjej[0] and siei[1] == sjej[1]:
        return 0
    if to_vec_dot(siei, sjej) <= 0:  # 90°≤α≤180°
        outD = np.sqrt(to_vec_dot(sjej, sjej))
    else:
        cos0 = to_vec_dot(siei, sjej) / (np.sqrt(to_vec_dot(siei, siei)) * np.sqrt(to_vec_dot(sjej, sjej)))
        if 1 - cos0 ** 2 > 0:
            sin0 = np.sqrt(1 - cos0**2)
        else:
            sin0 = 0
        outD = np.sqrt(to_vec_dot(sjej, sjej)) * sin0
    return outD


def lttilde(t_traj, start_ind, curr_ind):
    """cal L(T|T~)
    :param t_traj:
    :param start_ind:
    :param curr_ind:
    :return:
    """
    score1 = 0
    score2 = 0
    for j in range(start_ind, curr_ind):
        if t_traj[start_ind] == t_traj[j] and t_traj[curr_ind] == t_traj[j + 1]:
            continue
        # 更长的放前面
        if vlen(t_traj[start_ind], t_traj[curr_ind]) > vlen(t_traj[j], t_traj[j + 1]):
            presult = cal_perpendicular(t_traj[start_ind], t_traj[curr_ind], t_traj[j], t_traj[j + 1])
            aresult = angular(t_traj[start_ind], t_traj[curr_ind], t_traj[j], t_traj[j + 1])
        else:
            presult = cal_perpendicular(t_traj[j], t_traj[j + 1], t_traj[start_ind], t_traj[curr_ind])
            aresult = angular(t_traj[j], t_traj[j + 1], t_traj[start_ind], t_traj[curr_ind])
        score1 += presult
        score2 += aresult

    score1 = np.log2(score1) if score1 != 0 else 0
    score2 = np.log2(score2) if score2 != 0 else 0

    return score1 + score2


def Tmdl(t_traj):
    """generate func, see: Trajectory Clustering: A Partition-and-Group Framework
    计算得到的用代表点表示的轨迹
    :param t_traj:
    :return:
    """
    Tlen = len(t_traj)  # 原始的点数
    if Tlen == 0:
        return []
    CP = list()
    CP.append(t_traj[0])    # 存放初始轨迹点
    startIndex = 0      # 原点
    length = 1
    while startIndex + length < Tlen:
        currIndex = startIndex + length
        if lttilde(t_traj, startIndex, currIndex) > 0:
            CP.append(t_traj[currIndex - 1])
            startIndex = currIndex - 1
            length = 1
        else:
            length += 1
    CP.append(t_traj[-1])
    return CP


def mdl_main(min_latitude, min_longitude, init_path, base_path_list, preserve_path, rate=300, pid=0):
    """main func
    """
    # base_path_list = os.listdir(init_path)
    # tot_len = len(base_path_list)           # 有14650个
    # p = ProgressBar(tot_len, 'MDL轨迹简化')
    cnt = 0
    for path in base_path_list:
        # path = base_path_list[i]
        # p.update(i)
        # 打开独个轨迹数据
        with open(init_path + path, 'r') as file_object:
            T = []
            for line in file_object.readlines():
                jw = line.strip().split(',')
                w = float(jw[0].strip())
                j = float(jw[1].strip())
                T.append(((w - min_latitude)*rate, (j - min_longitude)*rate))       # 对轨迹点做映射
            t_tilde = Tmdl(T)      # 生成的轨迹
            # 查看生成的轨迹的长度，并检查有无空集
            if not len(t_tilde):
                print(init_path + path)
                print(T)
            with open(preserve_path + path.strip().split('.')[0] + '.txt', 'w') as f3:
                for item in t_tilde:
                    f3.writelines(str(item) + '\n')
            cnt += 1
            if cnt % 100 == 0:
                print('process: %d traj num %d' % (pid, cnt))


def cheak(path='../data/Geolife Trajectories 1.3/MDL/'):
    base_path_list = os.listdir(path)
    for i in range(len(base_path_list)):
        path_ = base_path_list[i]
        with open(path + path_, 'r') as file_object:
            if len(file_object.readlines()) == 0:
                print("空的：", path_)


def check_data(check_path='../data/Geolife Trajectories 1.3/MDL1200/'):
    length_ = []
    base_path_list = os.listdir(check_path)
    for path in base_path_list:
        file_object = open(check_path + path, 'r')
        length_.append(len(file_object.readlines()))
    print(length_[:20])
    print(np.mean(length_))
    print(np.std(length_, ddof=1))


if __name__ == '__main__':
    # 参数min_latitude, max_latitude, len_latitude纬度长度, min_longitude, max_longitude, len_longitude经度长度,
    # [39.4, 41.6, 115.7, 117.4] 总的轮廓 t_fullv2 953.054 1761.367  mdl_fullv2 40.952 56.869 1200
    # [39.7, 40.2, 116.0, 116.8] 最密集的地方 t_densev1 903.496 1658.663  mdl_densev1 38.368 51.333 1200
    # [39.7, 41.6, 115.7, 117.4] 最密集往左 t_leftv2 943.022 1789.898
    # [39.4, 40.2, 115.7, 117.4] 最密集往右 t_rightv1 910.620 1623.375
    # [39.4, 41.6, 116.0, 117.4] 最密集往上 t_upv1 951.595 1718.188
    # [39.4, 41.6, 115.7, 116.8] 最密集往下 t_downv1 937.325 1704.389
    base_path = '../data/Geolife Trajectories 1.3/t_leftv2/'
    new_path = '../data/Geolife Trajectories 1.3/mdl_leftv1/'
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    n_worker = 5
    base_path_list = os.listdir(base_path)
    Parallel(n_jobs=n_worker)(delayed(mdl_main)
                              (39.7, 116.0, base_path, fs, new_path, 1100, pid)
                              for fs, pid in zip(np.array_split(base_path_list, n_worker),
                                                 range(n_worker)))
    check_data(new_path)
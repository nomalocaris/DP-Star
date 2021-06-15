"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris、Giyn、HZT
# @File    : mdl.py
# @Software: PyCharm
-------------------------------------
"""

import os

import numpy as np
from joblib import Parallel
from joblib import delayed

from config import *
from utils import ProgressBar
from utils import equally_divide_list
from utils import to_vec_add
from utils import to_vec_dot
from utils import to_vec_sub
from utils import to_vec_times
from utils import vlen


def lt(t_traj, start_ind, curr_ind):
    """

    cal L(T~)

    Args:
        t_traj   :
        start_ind:
        curr_ind :

    Returns:
        length of T~

    """
    v_length = vlen(t_traj[start_ind], t_traj[curr_ind])

    return np.log2(v_length) if v_length else np.spacing(1)


def cal_perpendicular(si, ei, sj, ej):
    """

    Args:
        si:
        ei:
        sj:
        ej:

    Returns:
        outD:

    """
    si_sj = to_vec_sub(sj, si)
    si_ei = to_vec_sub(ei, si)
    si_ej = to_vec_sub(ej, si)
    _base = to_vec_dot(si_ei, si_ei)
    if _base == 0:
        return np.spacing(1)
    u1 = to_vec_dot(si_sj, si_ei) / _base
    u2 = to_vec_dot(si_ej, si_ei) / _base
    ps = to_vec_add(si, to_vec_times(u1, si_ei))
    pe = to_vec_add(si, to_vec_times(u2, si_ei))
    lp1 = vlen(ps, sj)
    lp2 = vlen(pe, ej)
    if lp1 + lp2 == 0:
        outD = 0
    else:
        outD = (lp1 ** 2 + lp2 ** 2) / (lp1 + lp2)

    return outD


def angular(si, ei, sj, ej):
    """

    cal angular distance

    Args:
        si:
        ei:
        sj:
        ej:

    Returns:
        outD:

    """
    si_ei = to_vec_sub(ei, si)
    sj_ej = to_vec_sub(ej, sj)
    if si_ei[0] == sj_ej[0] and si_ei[1] == sj_ej[1]:
        return 0
    # 90°≤α≤180°
    if to_vec_dot(si_ei, sj_ej) <= 0:
        outD = np.sqrt(to_vec_dot(sj_ej, sj_ej))
    else:
        cos0 = to_vec_dot(si_ei, sj_ej) / (np.sqrt(to_vec_dot(si_ei, si_ei)) *
                                           np.sqrt(to_vec_dot(sj_ej, sj_ej)))
        if 1 - cos0 ** 2 > 0:
            sin0 = np.sqrt(1 - cos0 ** 2)
        else:
            sin0 = 0
        outD = np.sqrt(to_vec_dot(sj_ej, sj_ej)) * sin0

    return outD


def lt_tilde(t_traj, start_ind, curr_ind):
    """

    cal L(T|T~)

    Args:
        t_traj   :
        start_ind:
        curr_ind :

    Returns:

    """
    score1 = 0
    score2 = 0
    for j in range(start_ind, curr_ind):
        if t_traj[start_ind] == t_traj[j] and t_traj[curr_ind] == t_traj[j + 1]:
            continue
        # longer put on the front
        if vlen(t_traj[start_ind], t_traj[curr_ind]) > vlen(t_traj[j], t_traj[j + 1]):
            p_result = cal_perpendicular(t_traj[start_ind], t_traj[curr_ind],
                                         t_traj[j], t_traj[j + 1])
            a_result = angular(t_traj[start_ind], t_traj[curr_ind], t_traj[j], t_traj[j + 1])
        else:
            p_result = cal_perpendicular(t_traj[j], t_traj[j + 1],
                                         t_traj[start_ind], t_traj[curr_ind])
            a_result = angular(t_traj[j], t_traj[j + 1], t_traj[start_ind], t_traj[curr_ind])
        score1 += p_result
        score2 += a_result

    score1 = np.log2(score1) if score1 != 0 else 0
    score2 = np.log2(score2) if score2 != 0 else 0

    return score1 + score2


def t_mdl(t_traj):
    """

    calculate trajectory represented by representative points

    Args:
        t_traj:

    Returns:

    """
    T_len = len(t_traj)  # original points
    if T_len == 0:
        return []

    CP = list()
    CP.append(t_traj[0])  # store initial trajectory points
    startIndex = 0  # origin point
    length = 1

    while startIndex + length < T_len:
        currIndex = startIndex + length
        if lt_tilde(t_traj, startIndex, currIndex) > 0:
            CP.append(t_traj[currIndex - 1])
            startIndex = currIndex - 1
            length = 1
        else:
            length += 1
    CP.append(t_traj[-1])

    return CP


def mdl_main(min_latitude: float, min_longitude: float, init_path: str, preserve_path: str,
             rate: int):
    """

    main func

    Args:
        min_latitude :
        min_longitude:
        init_path    :
        preserve_path:
        rate         :

    Returns:

    """
    if not os.path.exists(preserve_path):
        os.makedirs(preserve_path)

    tot_len = len(init_path)

    p = ProgressBar(tot_len, '基于MDL的轨迹简化')
    for i in range(tot_len):
        path = init_path[i]
        p.update(i)

        with open(preserve_path.replace('MDL', 'Trajectories') + path, 'r') as traj_file:
            T = []
            for line in traj_file.readlines():
                point = tuple(map(float, line.strip().split(',')))
                lat = point[0]
                lon = point[1]

                # mapping the trajectory points
                T.append(((lat - min_latitude) * rate, (lon - min_longitude) * rate))

            # generated trajectory
            t_tilde = t_mdl(T)

            with open(preserve_path + path.strip().split('.')[0] + '.txt', 'w') as file:
                for item in t_tilde:
                    file.writelines(str(item) + '\n')


def check_data():
    length_ = []
    files_list = os.listdir(f'../data/{USE_DATA}/SD/sd_final_epsilon_0.5/')
    for path in files_list:
        with open(f'../data/{USE_DATA}/SD/sd_final_epsilon_0.5/' + path, 'r') as file:
            length_.append(len(file.readlines()))
    print(length_)
    print(np.mean(length_))
    print(np.std(length_, ddof=1))


if __name__ == '__main__':
    trajs_file_list = os.listdir(f'../data/{USE_DATA}/Trajectories/')
    task_list = list(equally_divide_list(trajs_file_list, 7))

    Parallel(n_jobs=7)(delayed(mdl_main)(MIN_LAT_LON[USE_DATA][0], MIN_LAT_LON[USE_DATA][1],
                                         i, f'../data/{USE_DATA}/MDL/', MDL_SCALING_RATE[USE_DATA]
                                         ) for i in task_list)
    check_data()

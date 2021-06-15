"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : QG
# @File    : FP_KT.py
# @Software: PyCharm
-------------------------------------
"""

import os
import pickle

from joblib import Parallel
from joblib import delayed

from config import *

frequent_pattern_list = ['{}/frequent_pattern_raw.txt',
                         '{}/frequent_pattern_sd_{}.txt']


def save_frequent_pattern(trajs_path: str, min_latitude: float, min_longitude: float,
                          len_latitude: float, len_longitude: float, traj_type: str,
                          epsilon: float):
    """

    frequent patterns of stored data

    Args:
        trajs_path   : track file path
        min_latitude : minimum latitude(GPS)
        min_longitude: minimum longitude(GPS)
        len_latitude : latitude range(GPS)
        len_longitude: longitude range(GPS)
        traj_type    : choose a data set
        epsilon      : privacy budget

    Returns:
        sorted frequent pattern set

    """
    grid_side = 6
    if not os.path.exists(USE_DATA):
        os.mkdir(USE_DATA)

    each_lat = len_latitude / grid_side  # the span of the latitude side
    each_lon = len_longitude / grid_side  # the span of the longitude side

    frequent_pattern = {}  # frequent patterns

    trajs_file_list = os.listdir(trajs_path)
    for file in trajs_file_list:
        with open(trajs_path + file, 'r') as traj_file:
            grid_num_list = []
            for line in traj_file.readlines():
                point = list(map(float, line.split(',')))
                # latitude corresponds to the position of the grid
                lat_to_grid = int((point[0] - min_latitude) / each_lat)
                # longitude corresponds to the position of the grid
                lon_to_grid = int((point[1] - min_longitude) / each_lon)

                # exclude continuous occurrence in one grid
                if len(grid_num_list) > 0 and lat_to_grid * grid_side + lon_to_grid == grid_num_list[-1]:
                    continue
                if lat_to_grid * grid_side + lon_to_grid in grid_num_list:
                    continue

                grid_num_list.append(lat_to_grid * grid_side + lon_to_grid)  # number of the grid

        P = tuple(grid_num_list.copy())
        if len(P) >= 3:
            if P in frequent_pattern.keys():
                frequent_pattern[P] += 1
            else:
                frequent_pattern[P] = 1

    if traj_type == "raw":
        with open(frequent_pattern_list[0].format(USE_DATA), 'w') as file:
            for record in frequent_pattern.keys():
                file.writelines(str(record) + ':' + str(frequent_pattern[record]) + '\n')
    else:
        with open(frequent_pattern_list[1].format(USE_DATA, epsilon), 'w') as file:
            for record in frequent_pattern.keys():
                file.writelines(str(record) + ':' + str(frequent_pattern[record]) + '\n')

    return sorted(frequent_pattern.items(), key=lambda x: x[1], reverse=True)


def get_frequent_pattern(traj_type: str, epsilon: float) -> dict:
    """

    get frequent pattern data

    Args:
        traj_type: choose a data set
        epsilon  : privacy budget

    Returns:
        dict_: sorted frequent pattern set

    """
    frequent_pattern = {}
    if traj_type == "raw":
        with open(frequent_pattern_list[0].format(USE_DATA), 'r') as file:
            for line in file.readlines():
                frequent_pattern[tuple((line.split(':')[0].strip()[1:-1]).split(','))] = \
                    int(line.split(':')[1].strip())
    else:
        with open(frequent_pattern_list[1].format(USE_DATA, epsilon), 'r') as file:
            for line in file.readlines():
                frequent_pattern[tuple((line.split(':')[0].strip()[1:-1]).split(','))] = \
                    int(line.split(':')[1].strip())

    dict_ = {}
    for item in sorted(frequent_pattern.items(), key=lambda x: x[1], reverse=True):
        dict_[item[0]] = item[1]

    return dict_


def cal_fps(raw_trajs_frequent_pattern: dict, sd_trajs_frequent_pattern: dict) -> float:
    """

    calculate FPS

    Args:
        raw_trajs_frequent_pattern: frequent patterns of the original trajectory
        sd_trajs_frequent_pattern : frequent patterns that generate trajectories

    Returns:
        FPS

    """
    FP = 0

    for p in list(raw_trajs_frequent_pattern.keys())[:50]:
        if p in sd_trajs_frequent_pattern.keys():
            re = abs(raw_trajs_frequent_pattern[p] - sd_trajs_frequent_pattern[p]) / raw_trajs_frequent_pattern[p]
            FP += re

    return FP / 50


def cal_kt(raw_trajs_frequent_pattern, sd_trajs_frequent_pattern):
    """

    calculate KT

    Args:
        raw_trajs_frequent_pattern: frequent patterns of the original trajectory
        sd_trajs_frequent_pattern : frequent patterns that generate trajectories

    Returns:
        KT

    """
    concordant_count = 0
    discordant_count = 0
    k = 0

    for i in range(len(list(raw_trajs_frequent_pattern.keys()))):
        if k >= 50:
            break
        if list(raw_trajs_frequent_pattern.keys())[i] in sd_trajs_frequent_pattern.keys():
            k += 1

    for i in range(len(list(raw_trajs_frequent_pattern.keys())[:k])):
        if list(raw_trajs_frequent_pattern.keys())[i] in sd_trajs_frequent_pattern.keys():
            for j in range(i + 1, len(list(raw_trajs_frequent_pattern.keys())[:k])):
                if list(raw_trajs_frequent_pattern.keys())[j] in sd_trajs_frequent_pattern.keys():
                    if (raw_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[i]] >= raw_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[j]]
                        and sd_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[i]] > sd_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[j]]) \
                            or (raw_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[i]] < raw_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[j]]
                                and sd_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[i]] < sd_trajs_frequent_pattern[list(raw_trajs_frequent_pattern.keys())[j]]):
                        concordant_count += 1
                    else:
                        discordant_count += 1

    KT = (concordant_count - discordant_count) / (50 * 49 / 2)

    return KT


def run(epsilon):
    with open(f'../data/{USE_DATA}/GPS_trajs_range.pkl', 'rb') as GPS_trajs_range_file:
        GPS_trajs_range = pickle.loads(GPS_trajs_range_file.read())

    save_frequent_pattern(f'../data/{USE_DATA}/Trajectories/',
                          min_latitude=MIN_LAT_LON[USE_DATA][0],
                          min_longitude=MIN_LAT_LON[USE_DATA][1],
                          len_latitude=GPS_trajs_range[0][1] - GPS_trajs_range[0][0],
                          len_longitude=GPS_trajs_range[1][1] - GPS_trajs_range[1][0],
                          traj_type="raw", epsilon=epsilon)

    raw_trajs_frequent_pattern = get_frequent_pattern(traj_type="raw", epsilon=epsilon)

    save_frequent_pattern(f'../data/{USE_DATA}/SD/sd_final_epsilon_{epsilon}/',
                          min_latitude=MIN_LAT_LON[USE_DATA][0],
                          min_longitude=MIN_LAT_LON[USE_DATA][1],
                          len_latitude=GPS_trajs_range[0][1] - GPS_trajs_range[0][0],
                          len_longitude=GPS_trajs_range[1][1] - GPS_trajs_range[1][0],
                          traj_type="sd", epsilon=epsilon)

    sd_trajs_frequent_pattern = get_frequent_pattern(traj_type="sd", epsilon=epsilon)

    FP = cal_fps(raw_trajs_frequent_pattern, sd_trajs_frequent_pattern)
    KT = cal_kt(raw_trajs_frequent_pattern, sd_trajs_frequent_pattern)

    print('epsilon: %f. FP: %f. KT: %f' % (epsilon, FP, KT))


if __name__ == '__main__':
    Parallel(n_jobs=4)(delayed(run)(epsilon=i) for i in epsilon_list)

"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : QG
# @File    : query_avre.py
# @Software: PyCharm
-------------------------------------
"""

import pickle
import random

from joblib import Parallel
from joblib import delayed

from config import *
from metrics import *


def re(start_point: tuple, end_point: tuple, radius: float, raw_trajs: list,
       final_trajs: list) -> float:
    """

    calculate RE

    Args:
        start_point: range start
        end_point  : range end
        radius     : radius
        raw_trajs  : original trajectory
        final_trajs: generated trajectory

    Returns:
        RE

    """
    point_row = random.uniform(start_point[0], end_point[0])
    point_col = random.uniform(start_point[1], end_point[1])
    count_d = 0
    count_sd = 0
    b = int(len(raw_trajs) * 0.01)

    for i in range(len(raw_trajs)):
        for step in raw_trajs[i]:
            if (step[0] - point_row) ** 2 + (step[1] - point_col) ** 2 <= radius ** 2:
                count_d += 1
                break
        for step in final_trajs[i]:
            if (step[0] - point_row) ** 2 + (step[1] - point_col) ** 2 <= radius ** 2:
                count_sd += 1
                break

    RE = abs(count_d - count_sd) / max(count_d, b)

    return RE


def cal_re(raw_trajs: list, final_trajs: list, min_latitude: float, min_longitude: float,
           len_latitude: float, len_longitude: float, epsilon: float) -> float:
    """

    calculate RE

    Args:
        raw_trajs    : original trajectory
        final_trajs  : generated trajectory
        min_latitude : minimum latitude(GPS)
        min_longitude: minimum longitude(GPS)
        len_latitude : latitude range(GPS)
        len_longitude: longitude range(GPS)
        epsilon      : privacy budget

    Returns:
        RE: RE metric

    """
    error_r = 0
    # multiple average
    for it in range(10):
        error_r += re((min_latitude, min_longitude),
                      (min_latitude + len_latitude, min_longitude + len_longitude),
                      0.01, raw_trajs, final_trajs)

    query_avre = error_r / 10
    print('epsilon: ', epsilon, 'Query AvRE: ', query_avre)

    return query_avre


if __name__ == '__main__':
    with open(f'../data/{USE_DATA}/GPS_trajs_range.pkl', 'rb') as GPS_trajs_range_file:
        GPS_trajs_range = pickle.loads(GPS_trajs_range_file.read())

    raw_trajs_ = read_trajs_data(f'../data/{USE_DATA}/Trajectories/')

    Parallel(n_jobs=4)(delayed(cal_re)(raw_trajs=raw_trajs_,
                                       final_trajs=read_trajs_data(f'../data/{USE_DATA}/SD/sd_final_epsilon_{i}/'),
                                       min_latitude=MIN_LAT_LON[USE_DATA][0],
                                       min_longitude=MIN_LAT_LON[USE_DATA][1],
                                       len_latitude=GPS_trajs_range[0][1] - GPS_trajs_range[0][0],
                                       len_longitude=GPS_trajs_range[1][1] - GPS_trajs_range[1][0],
                                       epsilon=i) for i in epsilon_list)

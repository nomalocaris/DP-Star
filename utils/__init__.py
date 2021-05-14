#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
from ._progressbar import ProgressBar
from ._plot import plot_scatter, plot_traj
import os
import datetime
import numpy as np


def signum(x):
    """cal signum

    :param x:
    :return:
    """
    if x > 0:
        return 1.0
    if x < 0:
        return -1.0
    if x == 0:
        return 0


def vlen(pi1, pi2):
    """cal the distance between pi1 and pi2

    :param pi1:
    :param pi2:
    :return:
    """
    return ((pi1[0] - pi2[0]) ** 2 + (pi1[1] - pi2[1]) ** 2) ** 0.5


def traj_range(dpath='dataset/old/raw_trajs_pure/Trajectory/', dtype='common'):
    """计算轨迹的经纬度范围
    """
    trajfs = os.listdir(dpath)
    traj_fnum = len(trajfs)
    print(traj_fnum)
    if dtype == 'common':
        min_lon, min_lat = np.inf, np.inf
        max_lon, max_lat = -np.inf, -np.inf
    else:
        min_lon, min_lat = 180, 90
        max_lon, max_lat = -180, -90
    p = ProgressBar(traj_fnum, '计算经纬度范围')
    for i in range(traj_fnum):
        p.update(i)
        trajf = trajfs[i]
        with open(dpath + trajf) as fr:
            for line in fr.readlines():
                pos = list(map(float, line.replace('\n', '').split(',')))
                min_lon = pos[0] if pos[0] < min_lon else min_lon
                max_lon = pos[0] if pos[0] > max_lon else max_lon
                min_lat = pos[1] if pos[1] < min_lat else min_lat
                max_lat = pos[1] if pos[1] > max_lat else max_lat
    return [min_lon, max_lon], [min_lat, max_lat]


def cal_time_interval(prev_time, next_time):
    """cal the time interval, format: HH:MM:SS like 16:01:31

    :param prev_time:
    :param next_time:
    :return:
    """
    def split_time(t):
        """split and cal the time

        :param t:
        :return:
        """
        tta = t.split(':')
        t_hour = tta[0]
        t_mini = tta[1]
        t_sec = tta[2]

        return datetime.datetime(1, 1, 1, int(t_hour), int(t_mini), int(t_sec))

    prev_datetime = split_time(prev_time)
    next_datetime = split_time(next_time)

    return (next_datetime - prev_datetime).seconds

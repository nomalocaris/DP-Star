#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""包含一些对轨迹的处理函数"""
from __future__ import (absolute_import, unicode_literals)
import numpy as np
import os
from ._progressbar import ProgressBar


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





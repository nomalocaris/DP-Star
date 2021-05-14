#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
import datetime
from ._progressbar import ProgressBar
from ._vector_cal import to_vec_add, to_vec_sub, to_vec_times, to_vec_dot
from ._traj import traj_range


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


def vlen(pi1, pi2):
    """cal the distance between pi1 and pi2

    :param pi1:
    :param pi2:
    :return:
    """
    return ((pi1[0] - pi2[0]) ** 2 + (pi1[1] - pi2[1]) ** 2) ** 0.5


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
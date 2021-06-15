"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris、Giyn、HZT
# @File    : __init__.py
# @Software: PyCharm
-------------------------------------
"""

import datetime
import os
from math import ceil

import numpy as np

from ._progressbar import ProgressBar
from ._traj import trajs_range
from ._vector_cal import to_vec_add
from ._vector_cal import to_vec_dot
from ._vector_cal import to_vec_sub
from ._vector_cal import to_vec_times


def signum(x):
    """

    calculate signum

    Args:
        x: x

    Returns:
        signum

    """
    if x > 0:
        return 1.0
    if x < 0:
        return -1.0
    if x == 0:
        return 0


def vlen(pi1, pi2):
    """

    calculate the distance between pi1 and pi2

    Args:
        pi1: x
        pi2: x

    Returns:
        distance

    """
    return ((pi1[0] - pi2[0]) ** 2 + (pi1[1] - pi2[1]) ** 2) ** 0.5


def cal_time_interval(prev_time, next_time):
    """

    calculate the time interval, format: HH:MM:SS like 16:01:31

    Args:
        prev_time:
        next_time:

    Returns:


    """
    def split_time(t):
        """

        split and cal the time

        Args:
            t:

        Returns:

        """
        tta = t.split(':')
        t_hour = tta[0]
        t_mini = tta[1]
        t_sec = tta[2]

        return datetime.datetime(1, 1, 1, int(t_hour), int(t_mini), int(t_sec))

    prev_datetime = split_time(prev_time)
    next_datetime = split_time(next_time)

    return (next_datetime - prev_datetime).seconds


def equally_divide_list(lis, n):
    if n <= 0:
        yield lis
        return
    i, div = 0, ceil(len(lis) / n)
    while i < n:
        yield lis[i * div: (i + 1) * div]
        i += 1

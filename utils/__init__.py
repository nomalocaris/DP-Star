#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
from ._progressbar import ProgressBar


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

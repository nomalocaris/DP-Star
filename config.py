#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""
the config of parm for DP-Star
"""
from __future__ import (absolute_import, unicode_literals)

# privacy budget
epsilon = 1
# budget allocation
epsilon_alloc = {
    'ag': 1/9,  # adaptive Grid Construction
    'td': 3/9,  # trip distribution extraction
    'markov': 4/9,  # mobility model construction
    'mle': 1/9  # route length estimation(a median length estimation method)
}
#


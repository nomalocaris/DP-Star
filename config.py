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
    'ag': (1/9) * epsilon,  # adaptive Grid Construction
    'td': (3/9) * epsilon,  # trip distribution extraction
    'markov': (4/9) * epsilon,  # mobility model construction
    'mle': (1/9) * epsilon  # route length estimation(a median length estimation method)
}
# trajectory geo range
gps_range = {'lon': (0, 10), 'lat': (0, 10)}
# the number of the top grid
n_top_grid = 2
# a significant parm for adaptive grid, the smaller it is, the more bottom grid will be generate.
beta_factor = 0.3
# files path
idir_mdl_traj = 'data/Geolife Trajectories 1.3/representative_point'  # the mdl traj file
opath_top_grid = 'data/Geolife Trajectories 1.3/middleware/top_grid.txt'  # the ada grid construction
opath_grid_traj = 'data/Geolife Trajectories 1.3/middleware/grid_traj.txt'  # the grid-lized traj
opath_grid_block_gps_range = 'data/Geolife Trajectories 1.3/middleware/grid_block_gps_range.txt'  # the top grid range

#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""
the config of parm for DP-Star
"""
from __future__ import (absolute_import, unicode_literals)
import os

# privacy budget
epsilon = 0.1

# budget allocation
epsilon_alloc = {
    'ag': (1/9) * epsilon,  # adaptive Grid Construction
    'td': (3/9) * epsilon,  # trip distribution extraction
    'markov': (3/9) * epsilon,  # mobility model construction
    'mle': (2/9) * epsilon  # route length estimation(a median length estimation method)
}

# trajectory geo range
gps_range = {'lat': (0, 1320), 'lon': (0, 1760)}

# the number of the top grid
n_top_grid = 7

# a significant parm for adaptive grid, the smaller it is, the more bottom grid will be generate.
beta_factor = 80

# files path
idir_mdl_traj = 'data/Geolife Trajectories 1.3/MDL1100'  # the mdl traj file
# the ada grid construction
opath_top_grid = 'data/Geolife Trajectories 1.3/middleware/top_grid_MDL1100_ep' + str(epsilon) + '.txt'
# the grid-lized traj
opath_grid_traj = 'data/Geolife Trajectories 1.3/middleware/grid_traj_MDL1100_ep' + str(epsilon) + '.txt'
# the top grid range
omega_path = 'data/Geolife Trajectories 1.3/middleware/grid_block_gps_range_MDL1100_ep' + str(epsilon) + '.txt'
r_path = 'data/Geolife Trajectories 1.3/middleware/trip_distribution_MDL1100_ep' + str(epsilon) + '.txt'
x_path = 'data/Geolife Trajectories 1.3/middleware/midpoint_movement_MDL1100_ep' + str(epsilon) + '.txt'
l_path = 'data/Geolife Trajectories 1.3/middleware/length_traj_MDL1100_ep' + str(epsilon) + '.txt'
sd_path = 'data/Geolife Trajectories 1.3/middleware/sd_MDL1100_ep' + str(epsilon) + '.txt'  # grid-lized sd traj
sd_final_path = 'data/Geolife Trajectories 1.3/sd/sd_final_MDL1100_ep' + str(epsilon)  # ture sd traj dir

# create sd final path
if not os.path.exists(sd_final_path):
    os.makedirs(sd_final_path)



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

mdl_trajectories_input_dir = 'data/Geolife Trajectories 1.3/MDL1100'
# the ada grid construction
top_grid_path = f'data/Geolife Trajectories 1.3/middleware/top_grid_MDL1100_ep{epsilon}.txt'
# the grid trajectories
grid_trajectories_path = f'data/Geolife Trajectories 1.3/middleware/grid_traj_MDL1100_ep{epsilon}.txt'
# the top grid range
omega_path = f'data/Geolife Trajectories 1.3/middleware/grid_block_gps_range_MDL1100_ep{epsilon}.txt'
trip_distribution_path = f'data/Geolife Trajectories 1.3/middleware/trip_distribution_MDL1100_ep{epsilon}.txt'
midpoint_movement_path = f'data/Geolife Trajectories 1.3/middleware/midpoint_movement_MDL1100_ep{epsilon}.txt'
length_trajectories_path = f'data/Geolife Trajectories 1.3/middleware/length_traj_MDL1100_ep{epsilon}.txt'
# grid sd trajectories
sd_path = f'data/Geolife Trajectories 1.3/middleware/sd_MDL1100_ep{epsilon}.txt'
# ture sd trajectories dir
sd_final_path = f'data/Geolife Trajectories 1.3/sd/sd_final_MDL1100_ep{epsilon}.txt'

# create sd final path
# if not os.path.exists(sd_final_path):
#     os.makedirs(sd_final_path)

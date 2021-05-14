#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
from dpstar import generate_adaptive_grid
from dpstar import generate_sd_grid_mapping_traj
from dpstar import trip_distribution_main
from dpstar import mobility_model_main
from dpstar import route_length_estimate_main
from dpstar import syn

from config import *

# generate adaptive grid
n_grid = generate_adaptive_grid(
    idir_traj=idir_mdl_traj,
    opath_top_grid=opath_top_grid,
    opath_grid_traj=opath_grid_traj,
    opath_grid_block_gps_range=omega_path,
    n_top_grid=n_top_grid,
    epsilon_alloc=epsilon_alloc['ag'],
    epsilon_tot=epsilon,
    gps_range=gps_range,
    beta_factor=beta_factor
)
#
trip_distribution_main(n_grid, epsilon=epsilon_alloc['td'])
#
mobility_model_main(n_grid, epsilon=epsilon_alloc['markov'])
#
maxT = route_length_estimate_main(n_grid, epsilon=epsilon_alloc['mle'])
#
syn(n_grid, maxT)

# generate sd traj
generate_sd_grid_mapping_traj(
    ipath_sd=sd_path,
    n_top_grid=n_top_grid,
    ipath_top_grid=opath_top_grid,
    ipath_grid_block_gps_range=omega_path,
    odir_sd=sd_final_path,
    mapping_rate=1100,
    mapping_bais={'lat': 39.6, 'lon': 115.8}
)
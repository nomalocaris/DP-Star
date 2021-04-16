#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
from dpstar import generate_adaptive_grid
from config import *


# generate adaptive grid
n_grid = generate_adaptive_grid(
    idir_traj=idir_mdl_traj,
    opath_top_grid=opath_top_grid,
    opath_grid_traj=opath_grid_traj,
    opath_grid_block_gps_range=opath_grid_block_gps_range,
    n_top_grid=n_top_grid,
    epsilon_alloc=epsilon_alloc['ag'],
    epsilon_tot=epsilon,
    gps_range=gps_range,
    add_noise=False,
    beta_factor=beta_factor,
    is_plot=False
)

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
import numpy as np
import matplotlib.pyplot as plt

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
    # is_plot=True
)

trip_distribution_main(n_grid, epsilon=epsilon_alloc['td'])

mobility_model_main(n_grid, epsilon=epsilon_alloc['markov'])

maxT = route_length_estimate_main(n_grid, epsilon=epsilon_alloc['mle'])

syn(n_grid, maxT)

# # generate sd traj
# generate_sd_grid_mapping_traj(
#     ipath_sd=opath_sd_grid,
#     n_top_grid=n_top_grid,
#     ipath_top_grid=opath_top_grid,
#     ipath_grid_block_gps_range=opath_grid_block_gps_range,
#     odir_sd=opath_sd,
#     mapping_rate=300,
#     mapping_bais={'lat': 39.6, 'lon': 115.8}
# )

#
# tot_traj = read_mdl_data(idir_mdl_traj)
# plt.figure(figsize=(6, 5))
# for traj in tot_traj:
#     plt.plot([x[0] for x in traj], [y[1] for y in traj], c='blue')
#     plt.scatter([x[0] for x in traj], [y[1] for y in traj], c='blue')
# for traj in reverse_mapped_trajs:
#     plt.plot([x[0] for x in traj], [y[1] for y in traj], c='red')
#     plt.scatter([x[0] for x in traj], [y[1] for y in traj], c='red')
# # plot top gird lines
# top_gird_lines = cal_split(
#     (gps_range['lat'][0], gps_range['lat'][1]),
#     (gps_range['lon'][0], gps_range['lon'][1]),
#     n_top_grid)
# for line in top_gird_lines:
#     plt.plot([x[0] for x in line], [y[1] for y in line], c='black')
#
# # plot bottom grid lines
# for i in range(C):
#     if M[i] > 1:
#         bottom_grid_lines = cal_split(
#             (top_grid_block_gps_range[i][0][0], top_grid_block_gps_range[i][1][0]),
#             (top_grid_block_gps_range[i][0][1], top_grid_block_gps_range[i][1][1]),
#             M[i]
#         )
#         for line in bottom_grid_lines:
#             plt.plot([x[0] for x in line], [y[1] for y in line], c='black')
#     print(M[i])
# plt.xlim(gps_range['lat'][0], gps_range['lat'][1])
# plt.ylim(gps_range['lon'][1], gps_range['lon'][0])
# plt.xlabel('Lat')
# plt.ylabel('Lon')
# ax = plt.gca()
# ax.xaxis.set_ticks_position('top')
#
# plt.savefig('grid_traj')
# plt.show()

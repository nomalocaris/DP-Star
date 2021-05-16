#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
from dpstar import generate_adaptive_grid, read_mdl_data
from dpstar import generate_sd_grid_mapping_traj
from dpstar import trip_distribution_main
from dpstar import mobility_model_main
from dpstar import route_length_estimate_main
from dpstar import syn

from joblib import Parallel, delayed
from config import *
import numpy as np
import matplotlib.pyplot as plt

# privacy budget
epsilon_list = [0.1, 0.5, 1.0, 2.0]

# budget allocation
epsilon_alloc = {
    'ag': (1/9),  # adaptive Grid Construction
    'td': (3/9),  # trip distribution extraction
    'markov': (3/9),  # mobility model construction
    'mle': (2/9)  # route length estimation(a median length estimation method)
}


def run(epsilon):
    # generate adaptive grid
    n_grid = generate_adaptive_grid(
        idir_traj=mdl_trajectories_input_dir,
        opath_top_grid=top_grid_path,
        opath_grid_traj=grid_traj_path,
        opath_grid_block_gps_range=omega_path,
        n_top_grid=n_top_grid,
        epsilon_alloc=epsilon_alloc['ag'] * epsilon,
        epsilon_tot=epsilon,
        gps_range=gps_range,
        beta_factor=beta_factor
    )

    trip_distribution_main(n_grid, epsilon=epsilon_alloc['td'] * epsilon,
                           src_file=grid_traj_path, out_file=trip_distribution_path)

    mobility_model_main(n_grid, epsilon=epsilon_alloc['markov'] * epsilon,
                        src_file=grid_traj_path, out_file=midpoint_movement_path)

    maxT = route_length_estimate_main(n_grid, epsilon=epsilon_alloc['mle'] * epsilon,
                                      src_file=grid_traj_path, out_file=length_traj_path)

    syn(n_grid, maxT, trip_distribution_path, midpoint_movement_path, length_traj_path, sd_path, 14650)

    # generate sd trajectory
    generate_sd_grid_mapping_traj(
        ipath_sd=sd_path,
        n_top_grid=n_top_grid,
        ipath_top_grid=top_grid_path,
        ipath_grid_block_gps_range=omega_path,
        odir_sd=sd_final_path,
        mapping_rate=1100,
        mapping_bais={'lat': 39.6, 'lon': 115.8}
    )


if __name__ == '__main__':
    Parallel(n_jobs=4)(delayed(run)(i) for i in epsilon_list)

# tot_traj = read_mdl_data(idir_mdl_traj)
# tot_points = []
# for traj in tot_traj:
#     tot_points += traj
# tot_points = np.array(tot_points)
# print(tot_points.min(axis=0))
# print(tot_points.max(axis=0))

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

# plt.savefig('grid_traj')
# plt.show()

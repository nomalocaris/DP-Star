"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  :
             nomalocaris
             Giyn
# @File    : FP_KT.py
# @Software: PyCharm
-------------------------------------
"""

from dpstar import generate_adaptive_grid
from dpstar import generate_sd_grid_mapping_traj
from dpstar import trip_distribution_main
from dpstar import mobility_model_main
from dpstar import route_length_estimate_main
from dpstar import synthetic_trajs
from dpstar import read_mdl_data

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

mdl_trajs_dir = 'data/QG Taxi/MDL/'
# the ada grid construction
top_grid_path = 'data/QG Taxi/Middleware/top_grid_epsilon_{}.txt'
# the grid trajectories
grid_trajs_path = 'data/QG Taxi/Middleware/grid_trajs_epsilon_{}.txt'
# the top grid range
grid_block_gps_range_path = 'data/QG Taxi/Middleware/grid_block_gps_range_epsilon_{}.txt'
trip_distribution_path = 'data/QG Taxi/Middleware/trip_distribution_epsilon_{}.txt'
midpoint_movement_path = 'data/QG Taxi/Middleware/midpoint_movement_epsilon_{}.txt'
length_traj_path = 'data/QG Taxi/Middleware/routes_length_epsilon_{}.txt'
# grid sd trajectories
sd_path = 'data/QG Taxi/Middleware/sd_epsilon_{}'
# ture sd trajectories dir
sd_final_path = 'data/QG Taxi/SD/sd_final_epsilon_{}'


def run(epsilon):
    # generate adaptive grid
    n_grid = generate_adaptive_grid(
        mdl_trajs_dir=mdl_trajs_dir,
        top_grid_path=top_grid_path.format(epsilon),
        grid_trajs_path=grid_trajs_path.format(epsilon),
        grid_block_gps_range_path=grid_block_gps_range_path.format(epsilon),
        n_top_grid=n_top_grid,
        epsilon_alloc=epsilon_alloc['ag'] * epsilon,
        epsilon_total=epsilon,
        gps_range=gps_range,
        beta_factor=beta_factor
    )

    trip_distribution_main(n_grid, _epsilon=epsilon_alloc['td'] * epsilon,
                           grid_trajs_path=grid_trajs_path.format(epsilon),
                           trip_distribution_path=trip_distribution_path.format(epsilon))

    mobility_model_main(n_grid, _epsilon=epsilon_alloc['markov'] * epsilon,
                        grid_trajs_path=grid_trajs_path.format(epsilon),
                        midpoint_movement_path=midpoint_movement_path.format(epsilon))

    maxT = route_length_estimate_main(n_grid, _epsilon=epsilon_alloc['mle'] * epsilon,
                                      grid_trajs_path=grid_trajs_path.format(epsilon),
                                      routes_length_path=length_traj_path.format(epsilon))

    synthetic_trajs(n_grid, maxT, trip_distribution_path.format(epsilon),
                    midpoint_movement_path.format(epsilon), length_traj_path.format(epsilon),
                    sd_path.format(epsilon), 2801)

    # generate sd trajectory
    generate_sd_grid_mapping_traj(
        sd_path=sd_path.format(epsilon),
        grid_block_gps_range_path=grid_block_gps_range_path.format(epsilon),
        sd_desensitize_path=sd_final_path.format(epsilon),
        mapping_rate=1200,
        mapping_bias={'lat': 22.8, 'lon': 112.7}
    )


if __name__ == '__main__':
    Parallel(n_jobs=4)(delayed(run)(i) for i in epsilon_list)

    # tot_traj = read_mdl_data(mdl_trajectories_input_dir)
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

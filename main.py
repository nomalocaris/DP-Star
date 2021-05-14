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
from dpstar import read_mdl_data

import utils
from config import *
import numpy as np
import matplotlib.pyplot as plt
#
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

# tot_traj = read_mdl_data(idir_mdl_traj)
# tot_points = []
# for traj in tot_traj:
#     tot_points += traj
# tot_points = np.array(tot_points)
# print(tot_points.min(axis=0))
# print(tot_points.max(axis=0))

tot_len = 0
with open(sd_path) as fr:
    tot_traj = [eval(t) for t in fr.readlines()]
for t in tot_traj:
    tot_len += len(t)
print('脱敏网格数据总长度: %.4f, 平均长度: %.4f' % (tot_len, tot_len/len(tot_traj)))


tot_traj = read_mdl_data('data/Geolife Trajectories 1.3/sd/sd_final_MDL1100_ep'+str(epsilon))
avg_len = 0
for traj in tot_traj:
    avg_len += len(traj)
print('脱敏数据总长度: %.4f, 平均长度: %.4f' % (avg_len, avg_len/len(tot_traj)))

avg_len = 0
tot_sd_traj = read_mdl_data('data/Geolife Trajectories 1.3/Trajectories7000/')
for traj in tot_sd_traj:
    avg_len += len(traj)
avg_len /= len(tot_traj)
print('平均长度: %.4f' % avg_len)

avg_len = 0
tot_sd_traj = read_mdl_data(idir_mdl_traj)
for traj in tot_sd_traj:
    avg_len += len(traj)
avg_len /= len(tot_traj)
print('平均长度: %.4f' % avg_len)
# utils.plot_traj(trajs=tot_sd_traj, od_only=True, title='origin data', size=0.5)


# tot_sd_points = []
# for traj in tot_sd_traj:
#     tot_sd_points += traj
# utils.plot_scatter(points=tot_sd_points)

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

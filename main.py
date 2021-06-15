"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris
             Giyn
# @File    : main.py
# @Software: PyCharm
-------------------------------------
"""

from joblib import Parallel, delayed

from config import *
from dp_star import generate_adaptive_grid
from dp_star import generate_sd_grid_mapping_traj
from dp_star import mobility_model_main
from dp_star import route_length_estimate_main
from dp_star import synthetic_trajs
from dp_star import trip_distribution_main


mdl_trajs_path = 'data/{}/MDL/'
top_grid_path = 'data/{}/Middleware/top_grid_epsilon_{}.txt'
grid_trajs_path = 'data/{}/Middleware/grid_trajs_epsilon_{}.txt'
grid_block_gps_range_path = 'data/{}/Middleware/grid_block_gps_range_epsilon_{}.txt'
trip_distribution_path = 'data/{}/Middleware/trip_distribution_epsilon_{}.txt'
midpoint_movement_path = 'data/{}/Middleware/midpoint_movement_epsilon_{}.txt'
length_traj_path = 'data/{}/Middleware/routes_length_epsilon_{}.txt'
sd_path = 'data/{}/SD/sd_epsilon_{}.txt'
sd_final_path = 'data/{}/SD/sd_final_epsilon_{}'


def run(epsilon):
    if not os.path.exists(f'data/{USE_DATA}/Middleware'):
        os.mkdir(f'data/{USE_DATA}/Middleware')

    # generate adaptive grid
    n_grid = generate_adaptive_grid(
        mdl_trajs_dir=mdl_trajs_path.format(USE_DATA),
        top_grid_path=top_grid_path.format(USE_DATA, epsilon),
        grid_trajs_path=grid_trajs_path.format(USE_DATA, epsilon),
        grid_block_gps_range_path=grid_block_gps_range_path.format(USE_DATA, epsilon),
        n_top_grid=n_top_grid,
        epsilon_alloc=epsilon_alloc['ag'] * epsilon,
        epsilon_total=epsilon,
        gps_range=gps_range,
        beta_factor=beta_factor
    )

    trip_distribution_main(n_grid, _epsilon=epsilon_alloc['td'] * epsilon,
                           grid_trajs_path=grid_trajs_path.format(USE_DATA, epsilon),
                           trip_distribution_path=trip_distribution_path.format(USE_DATA, epsilon))

    mobility_model_main(n_grid, _epsilon=epsilon_alloc['markov'] * epsilon,
                        grid_trajs_path=grid_trajs_path.format(USE_DATA, epsilon),
                        midpoint_movement_path=midpoint_movement_path.format(USE_DATA, epsilon))

    maxT = route_length_estimate_main(n_grid, _epsilon=epsilon_alloc['mle'] * epsilon,
                                      grid_trajs_path=grid_trajs_path.format(USE_DATA, epsilon),
                                      routes_length_path=length_traj_path.format(USE_DATA, epsilon))

    if not os.path.exists(f'data/{USE_DATA}/SD'):
        os.mkdir(f'data/{USE_DATA}/SD')

    synthetic_trajs(n_grid, maxT, trip_distribution_path.format(USE_DATA, epsilon),
                    midpoint_movement_path.format(USE_DATA, epsilon), length_traj_path.format(USE_DATA, epsilon),
                    sd_path.format(USE_DATA, epsilon), TRAJS_NUM[USE_DATA])

    # generate sd trajectory
    generate_sd_grid_mapping_traj(
        sd_path=sd_path.format(USE_DATA, epsilon),
        grid_block_gps_range_path=grid_block_gps_range_path.format(USE_DATA, epsilon),
        sd_final_path=sd_final_path.format(USE_DATA, epsilon),
        mapping_rate=MDL_SCALING_RATE[USE_DATA],
        mapping_bias=mapping_bias
    )


if __name__ == '__main__':
    Parallel(n_jobs=4)(delayed(run)(i) for i in epsilon_list)

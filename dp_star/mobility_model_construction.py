"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 12:03:46
# @Author  : Giyn
# @Email   : giyn.jy@gmail.com
# @File    : mobility_model_construction.py
# @Software: PyCharm
-------------------------------------
"""

import numpy as np

from utils import ProgressBar


def markov_model(trajs: list, n_grid: int, _epsilon: float) -> np.ndarray:
    """

    markov model

    Args:
        trajs   : trajectory data
        n_grid  : number of secondary grids
        _epsilon: privacy budget

    Returns:
        O_: intermediate point transition probability matrix

    """
    O_ = np.zeros((n_grid, n_grid))  # establish n_grid * n_grid transition probability matrix
    for t in trajs:
        O_sub = np.zeros((n_grid, n_grid))
        for i in range(len(t) - 1):
            curr_point = t[i]
            next_point = t[i + 1]
            O_sub[curr_point][next_point] += 1
        O_sub /= (len(t) - 1)  # transition probability of the trajectory
        O_ += O_sub

    p = ProgressBar(n_grid, 'Generate midpoint transition probability matrix')
    for i in range(n_grid):
        p.update(i)
        for j in range(n_grid):
            noise = np.random.laplace(0, 1 / _epsilon)  # add laplacian noise
            O_[i][j] += noise

            if O_[i][j] < 0:
                O_[i][j] = 0

    # compute X
    row_sum = [sum(O_[i]) for i in range(n_grid)]
    for j in range(n_grid):
        O_[j] /= row_sum[j]

    return O_


def mobility_model_main(n_grid: int, _epsilon: float, grid_trajs_path: str,
                        midpoint_movement_path: str):
    """

    main function

    Args:
        n_grid                : number of grids
        _epsilon              : privacy budget
        grid_trajs_path       : grid track file path
        midpoint_movement_path: midpoint transition probability matrix file path

    Returns:

    """
    with open(grid_trajs_path, 'r') as grid_trajs_file:
        T = [eval(traj) for traj in grid_trajs_file.readlines()]
        with open(midpoint_movement_path, 'w') as midpoint_movement_file:
            midpoint_movement_matrix = markov_model(T, n_grid, _epsilon)
            for item in midpoint_movement_matrix:
                each_line = ' '.join([str(i) for i in item]) + '\n'
                midpoint_movement_file.writelines(each_line)


if __name__ == '__main__':
    epsilon = 0.1
    mobility_model_main(64, epsilon * 3 / 9,
                        f'../data/Geolife Trajectories 1.3/Middleware/grid_trajs_epsilon_{epsilon}.txt',
                        f'../data/Geolife Trajectories 1.3/Middleware/midpoint_movement_epsilon_{epsilon}.txt')

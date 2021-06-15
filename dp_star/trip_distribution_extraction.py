"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 11:57:44
# @Author  : Giyn
# @Email   : giyn.jy@gmail.com
# @File    : trip_distribution_extraction.py
# @Software: PyCharm
-------------------------------------
"""

import numpy as np

from utils import ProgressBar


def trip_distribution(trajs: list, n_grid: int, _epsilon: float) -> np.ndarray:
    """

    get the transition probability matrix

    Args:
        trajs   : trajectory data(two dimensional array)
        n_grid  : number of secondary grids
        _epsilon: privacy budget

    Returns:
        R: transition probability matrix

    """
    R = np.zeros((n_grid, n_grid))  # establish n_grid * n_grid transition probability matrix
    for t in trajs:
        if len(t) > 1:
            sta = t[0]
            end = t[-1]
            R[sta][end] += 1

    count = int(np.sum(R))  # number of tracks

    p = ProgressBar(n_grid, 'Generate transition probability matrix')
    for i in range(n_grid):
        p.update(i)
        for j in range(n_grid):
            noise = np.random.laplace(0, 1 / _epsilon)  # add laplacian noise
            R[i][j] += noise

            if R[i][j] < 0:
                R[i][j] = 0

    R /= count

    return R


def trip_distribution_main(n_grid: int, _epsilon: float, grid_trajs_path: str,
                           trip_distribution_path: str):
    """

    trip distribution (main function)

    Args:
        n_grid                : number of grids
        _epsilon              : privacy budget
        grid_trajs_path       : grid trajectory file path
        trip_distribution_path: transition probability matrix output file path

    Returns:

    """
    with open(grid_trajs_path, 'r') as grid_trajs_file:
        T = [eval(grid_traj) for grid_traj in grid_trajs_file.readlines()]
        with open(trip_distribution_path, 'w') as trip_distribution_file:
            trip_distribution_matrix = trip_distribution(T, n_grid, _epsilon)
            for item in trip_distribution_matrix:
                each_line = ' '.join([str(i) for i in item]) + '\n'
                trip_distribution_file.writelines(each_line)


if __name__ == '__main__':
    epsilon = 0.1
    trip_distribution_main(64, 0.1 * 3 / 9,
                           f'../data/Geolife Trajectories 1.3/Middleware/grid_trajs_epsilon_{epsilon}.txt',
                           f'../data/Geolife Trajectories 1.3/Middleware/trip_distribution_epsilon_{epsilon}.txt')

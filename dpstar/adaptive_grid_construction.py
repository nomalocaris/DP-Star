#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""
    The components of DP-Star: Adaptive grid construction.
"""
from __future__ import (absolute_import, unicode_literals)
import os
import utils
import numpy as np
import matplotlib.pyplot as plt


def read_mdl_data(idir_traj):
    """Read the mdl data according to the idir_path
    """
    # get the traj files
    traj_files = os.listdir(idir_traj)
    assert len(traj_files) > 0, 'There is no trajectory.'

    # read trajs
    trajs = []
    for traj_file in traj_files:
        with open(idir_traj + '/' + traj_file) as f_mdl_traj:
            # _traj = [list(map(float, _point.replace('\n', '').split(','))) for _point in f_mdl_traj.readlines()]
            _traj = [eval(_point) for _point in f_mdl_traj.readlines()]
            trajs.append(_traj)

    return trajs


def generate_adaptive_grid(
        idir_traj, opath_top_grid, opath_grid_traj, opath_grid_block_gps_range, epsilon_alloc, epsilon_tot, gps_range,
        n_top_grid=7, add_noise=True, is_plot=False, beta_factor=80
):
    """
    As the name suggests.
    :param idir_traj: input dir for trajectory in which traj is like (lat, lon)
    :param opath_top_grid: output path for the top grid partition.
    :param opath_grid_traj: output path for the grid partition traj.
    :param opath_grid_block_gps_range: output path for the grid range.
    :param n_top_grid: the number of top grid.
    :param epsilon_alloc: the pravacy budget of adaptive grid.
    :param epsilon_tot: the pravacy budget of DP-Star.
    :param gps_range: the gps range of traj which has a format like {'lon':(lon_min, lon_max), 'lat':(lat_min, lat_max)}
    :param add_noise: whether add noise in grid or not.
    :param is_plot: whether plot the gps point and grid.
    :param beta_factor:
    :return:
    """

    def grid_boundary_judge(cal_grid_idx, boundary=n_top_grid):
        """judge the calculated gird idx is out of the grid boundary
        like the n_top_grip is 7, but the calculated idx is 7 because its position at the edge of grip.
        under this situation, we simply choose its idx equal the n_top_grip - 1.
        """
        return cal_grid_idx if cal_grid_idx < boundary else boundary - 1

    assert len(gps_range) == 2, 'The format of gps_range is wrong!'

    def cal_point_idx(_point, _n_grid=n_top_grid, _step=None, _base=None):
        """
        cal the idx of point in grid
        :param _point: the point which need to caled
        :param _n_grid: the number of grid
        :param _step: the gird block length
        :param _base: the bias or basic of the point
        :return:
        """
        idx = grid_boundary_judge(int((_point[0]-_base['lat']) / _step['lat']), _n_grid) * _n_grid \
            + grid_boundary_judge(int((_point[1]-_base['lon']) / _step['lon']), _n_grid)

        return idx

    tot_traj = read_mdl_data(idir_traj)
    # grid parm according to the paper.
    beta = (epsilon_tot - epsilon_alloc) / beta_factor
    # the block num of top gird
    C = n_top_grid ** 2
    # the gps range for each top grid block
    top_block_gps_step = {
        'lon': (gps_range['lon'][1] - gps_range['lon'][0]) / n_top_grid,
        'lat': (gps_range['lat'][1] - gps_range['lat'][0]) / n_top_grid
    }
    # cal the eta score for each top grid
    eta_score = [0 for _ in range(C)]
    for traj in tot_traj:
        for point in traj:
            C_idx = cal_point_idx(point, _step=top_block_gps_step,
                                  _base={'lon': gps_range['lon'][0], 'lat': gps_range['lat'][0]})
            eta_score[C_idx] += 1 / len(traj) if len(traj) else 0
    # add lap noise
    if add_noise:
        lap_noise = np.random.laplace(0, 1 / epsilon_alloc, C)
        eta_score = [eta_score[i] + lap_noise[i] for i in range(C)]
        # puzzle: simple let the minus values equal 0
        for i in range(C):
            if eta_score[i] < 0:
                eta_score[i] = 0
    # the bottom gir num for each top grid block
    M = [np.sqrt(eta_score[i] * beta) for i in range(C)]
    for i in range(C):
        if M[i] < 1:
            # min grid num is 1
            M[i] = 1
        else:
            # rounding
            M[i] = int(np.rint(M[i]))

    # cal the grid range
    grid_block_gps_range = {}
    for i in range(C):
        current_idx = 0
        for j in range(i):
            # get the current idx
            current_idx += M[j] ** 2
        # if there is only one grid.
        if M[i] == 1:
            row = i // n_top_grid
            col = i - row * n_top_grid
            grid_block_gps_range[current_idx] = (
                ((row * top_block_gps_step['lat'] + gps_range['lat'][0],
                  col * top_block_gps_step['lon'] + gps_range['lon'][0]),
                 ((row + 1) * top_block_gps_step['lat'] + gps_range['lat'][0],
                  (col + 1) * top_block_gps_step['lon'] + gps_range['lon'][0]))
            )
        # if there are not only one grid.
        else:
            row = i // n_top_grid
            col = i - row * n_top_grid
            start_point = (row * top_block_gps_step['lat'] + gps_range['lat'][0],
                           col * top_block_gps_step['lon'] + gps_range['lon'][0])
            end_point = ((row + 1) * top_block_gps_step['lat'] + gps_range['lat'][0],
                         (col + 1) * top_block_gps_step['lon'] + gps_range['lon'][0])
            for k in range(M[i]**2):
                bottom_block_gps_step = {
                    'lat': (end_point[0] - start_point[0]) / M[i],
                    'lon': (end_point[1] - start_point[1]) / M[i]
                }
                row = k // M[i]
                col = k - row * M[i]
                grid_block_gps_range[current_idx+k] = (
                    ((row * bottom_block_gps_step['lat'] + start_point[0],
                      col * bottom_block_gps_step['lon'] + start_point[1]),
                     ((row + 1) * bottom_block_gps_step['lat'] + start_point[0],
                      (col + 1) * bottom_block_gps_step['lon'] + start_point[1]))
                )

    # print(grid_block_gps_range)
    # cal the top grid range
    top_grid_block_gps_range = []
    for i in range(C):
        row = i // n_top_grid
        col = i - row * n_top_grid
        top_grid_block_gps_range.append(
            ((row * top_block_gps_step['lat'] + gps_range['lat'][0],
              col * top_block_gps_step['lon'] + gps_range['lon'][0]),
             ((row + 1) * top_block_gps_step['lat'] + gps_range['lat'][0],
              (col + 1) * top_block_gps_step['lon'] + gps_range['lon'][0]))
        )

    # cal the grid num
    n_grid = 0
    for i in range(C):
        n_grid += M[i] ** 2
    print('总网格数: %d' % n_grid)

    # write to file
    with open(opath_top_grid, 'w') as fw_top_grid:
        fw_top_grid.writelines(str(M))
    with open(opath_grid_block_gps_range, 'w') as fw_grid_block_range:
        fw_grid_block_range.write(str(grid_block_gps_range)+'\n')
        fw_grid_block_range.write(str(top_grid_block_gps_range) + '\n')

    # map the traj into the grid
    p = utils.ProgressBar(len(tot_traj), '映射网格轨迹')
    mapped_trajs = []
    for i in range(len(tot_traj)):
        p.update(i)
        mapped_traj = []
        for point in tot_traj[i]:
            # cal the idx in the top grid
            # C_idx = cal_point_idx(point, _step=top_block_gps_step,
            #                       _base={'lon': gps_range['lon'][0], 'lat': gps_range['lat'][0]})
            #
            # # cal the idx in the bottom grid
            # m = M[C_idx]
            # for j in range(C_idx):
            #     # add the privious bottom grid num.
            #     C_idx += M[j] ** 2 if M[j] == 1 else M[j] ** 2 - 1
            for k in range(n_grid):
                grid_range = grid_block_gps_range[k]
                if grid_range[1][0] >= point[0] >= grid_range[0][0] and \
                   grid_range[1][1] >= point[1] >= grid_range[0][1]:
                    mapped_traj.append(k)

        mapped_trajs.append(mapped_traj)

    # # reverse map to grid
    # reverse_mapped_trajs = []
    # for traj in mapped_trajs:
    #     reverse_mapped_trajs.append([np.mean(grid_block_gps_range[i], axis=0).tolist() for i in traj])
    # print(reverse_mapped_trajs)

    # write to file
    with open(opath_grid_traj, 'w') as fw_grid_traj:
        for mt in mapped_trajs:
            fw_grid_traj.writelines(str(mt)+'\n')

    # plot the figure
    if is_plot:
        plt.figure(figsize=(6, 5))
        p = utils.ProgressBar(len(tot_traj), '绘制网格轨迹图')
        for i in range(len(tot_traj)):
            p.update(i)
            plt.plot([x[0] for x in tot_traj[i]], [y[1] for y in tot_traj[i]])
            plt.scatter([x[0] for x in tot_traj[i]], [y[1] for y in tot_traj[i]])
        # plot top gird lines
        top_gird_lines = cal_split(
            (gps_range['lat'][0], gps_range['lat'][1]),
            (gps_range['lon'][0], gps_range['lon'][1]),
            n_top_grid)
        for line in top_gird_lines:
            plt.plot([x[0] for x in line], [y[1] for y in line], c='black')

        # plot bottom grid lines
        for i in range(C):
            if M[i] > 1:
                bottom_grid_lines = cal_split(
                    (top_grid_block_gps_range[i][0][0], top_grid_block_gps_range[i][1][0]),
                    (top_grid_block_gps_range[i][0][1], top_grid_block_gps_range[i][1][1]),
                    M[i]
                )
                for line in bottom_grid_lines:
                    plt.plot([x[0] for x in line], [y[1] for y in line], c='black')
            print(M[i])
        plt.xlim(gps_range['lat'][0], gps_range['lat'][1])
        plt.ylim(gps_range['lon'][1], gps_range['lon'][0])
        plt.xlabel('Lat')
        plt.ylabel('Lon')
        ax = plt.gca()
        ax.xaxis.set_ticks_position('top')

        plt.savefig('grid_traj')
        plt.show()
    return n_grid


def cal_split(x_range, y_range, n_split):
    """grid split for plot
    """
    x_range_step = (x_range[1] - x_range[0]) / n_split
    y_range_step = (y_range[1] - y_range[0]) / n_split
    split_lines = []
    for i in range(1, n_split):
        split_lines += [(
                (x_range[0] + x_range_step * i, y_range[0]),
                (x_range[0] + x_range_step * i, y_range[1])
            ),
            (
                (x_range[0], y_range[0]+y_range_step*i),
                (x_range[1], y_range[0] + y_range_step * i)
            )]
    return split_lines


def generate_sd_grid_mapping_traj(
    ipath_sd, n_top_grid, ipath_top_grid, ipath_grid_block_gps_range, odir_sd,
    mapping_rate=1, mapping_bais=None
):
    """generate the gird-mapping traj for SD
    """
    # for pep8
    if mapping_bais is None:
        mapping_bais = {'lat': 0, 'lon': 0}

    # privacy budget
    with open(ipath_sd) as fr_sd:
        sd = [eval(point.replace('\n', '')) for point in fr_sd.readlines()]
    print(len(sd))
    # C = n_top_grid ** 2
    # with open(ipath_top_grid) as fr_top_grid:
    #     M = eval(fr_top_grid.readline())

    with open(ipath_grid_block_gps_range) as fr_top_grid_block_gps_range:
        fstr = fr_top_grid_block_gps_range.readlines()
        grid_block_gps_range = eval(fstr[0])
        # top_grid_block_gps_range = eval(fstr[1])

    reverse_mapped_trajs = []
    for traj in sd:
        print(traj)
        reverse_mapped_trajs.append([list(np.mean(grid_block_gps_range[i], axis=0)) for i in traj])

    # write to files
    fcount = 0
    for traj in reverse_mapped_trajs:
        with open(odir_sd + '/sd_traj' + str(fcount) + '.txt', 'w') as fw_traj:
            for point in traj:
                # mapping
                point = [point[0]/mapping_rate+mapping_bais['lat'], point[1]/mapping_rate+mapping_bais['lon']]
                fw_traj.write(str(point[0])+','+str(point[1])+'\n')
            fcount += 1

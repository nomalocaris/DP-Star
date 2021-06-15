"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris、Giyn、HZT
# @File    : adaptive_grid_construction.py
# @Software: PyCharm
-------------------------------------
"""

import matplotlib.pyplot as plt
import numpy as np
from config import *
import utils


def read_mdl_data(mdl_trajs_dir):
    """

    Read the mdl data according to the idir_path

    Args:
        mdl_trajs_dir: MDL轨迹文件夹

    Returns:
        trajs: MDL轨迹数据(list)

    """
    # get the traj files
    traj_files = os.listdir(mdl_trajs_dir)
    assert len(traj_files) > 0, 'There is no trajectory.'

    # read trajs
    trajs = []
    for traj_file in traj_files:
        with open(mdl_trajs_dir + '/' + traj_file) as each_mdl_traj:
            traj = [eval(point) for point in each_mdl_traj.readlines()]
            trajs.append(traj)

    return trajs


def generate_adaptive_grid(mdl_trajs_dir, top_grid_path, grid_trajs_path,
                           grid_block_gps_range_path, epsilon_alloc, epsilon_total, gps_range,
                           n_top_grid=7, add_noise=True, is_plot=False, beta_factor=80):
    """

    As the name suggests.

    Args:
        mdl_trajs_dir             : input dir for trajectory in which traj is like (lat, lon)
        top_grid_path             : output path for the top grid partition.
        grid_trajs_path           : output path for the grid partition traj.
        grid_block_gps_range_path : output path for the grid range.
        n_top_grid                : the number of top grid.
        epsilon_alloc             : the privacy budget of adaptive grid.
        epsilon_total             : the privacy budget of DP-Star.
        gps_range                 : the gps range of traj which has a format like
                                    {'lon':(lon_min, lon_max), 'lat':(lat_min, lat_max)}
        add_noise                 : whether add noise in grid or not.
        is_plot                   : whether plot the gps point and grid.
        beta_factor               :

    Returns:
        n_grid: 网格数

    """

    def grid_boundary_judge(cal_grid_idx, boundary=n_top_grid):
        """judge the calculated gird idx is out of the grid boundary

        like the n_top_grid is 7, but the calculated idx is 7 because its position at the edge of grid.
        under this situation, we simply choose its idx equal the n_top_grid - 1.

        """

        return cal_grid_idx if cal_grid_idx < boundary else boundary - 1

    assert len(gps_range) == 2, 'The format of gps_range is wrong!'

    def cal_point_idx(_point, _n_grid=n_top_grid, _step=None, _base=None):
        """

        cal the idx of point in grid

        Args:
            _point: the point which need to caled
            _n_grid: the number of grid
            _step: the gird block length
            _base: the bias or basic of the point

        Returns:
            idx: 网格点的索引

        """
        idx = grid_boundary_judge(int((_point[0] - _base['lat']) / _step['lat']),
                                  _n_grid) * _n_grid + grid_boundary_judge(
            int((_point[1] - _base['lon']) / _step['lon']), _n_grid)

        return idx

    total_trajs = read_mdl_data(mdl_trajs_dir)

    # grid parm according to the paper.
    beta = (epsilon_total - epsilon_alloc) / beta_factor

    # the block num of top gird
    C = n_top_grid ** 2

    # the gps range for each top grid block
    top_block_gps_step = {
        'lon': (gps_range['lon'][1] - gps_range['lon'][0]) / n_top_grid,
        'lat': (gps_range['lat'][1] - gps_range['lat'][0]) / n_top_grid
    }

    # calculate the eta score for each top grid
    eta_score = [0 for _ in range(C)]
    for traj in total_trajs:
        for point in traj:
            C_idx = cal_point_idx(point, _step=top_block_gps_step,
                                  _base={'lon': gps_range['lon'][0], 'lat': gps_range['lat'][0]})
            eta_score[C_idx] += 1 / len(traj) if len(traj) else 0

    # add laplace noise
    if add_noise:
        laplace_noise = np.random.laplace(0, 1 / epsilon_alloc, C)
        eta_score = [eta_score[i] + laplace_noise[i] for i in range(C)]

        # puzzle: simple let the minus values equal 0
        for i in range(C):
            if eta_score[i] < 0:
                eta_score[i] = 0

    # the bottom gird num for each top grid block
    M = [np.sqrt(eta_score[i] * beta) for i in range(C)]
    for i in range(C):
        if M[i] < 1:
            M[i] = 1  # min grid num is 1
        else:
            M[i] = int(np.rint(M[i]))  # rounding

    # calculate the grid range
    grid_block_gps_range = {}
    for i in range(C):
        current_idx = 0
        for j in range(i):
            current_idx += M[j] ** 2  # get the current index

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
            for k in range(M[i] ** 2):
                bottom_block_gps_step = {
                    'lat': (end_point[0] - start_point[0]) / M[i],
                    'lon': (end_point[1] - start_point[1]) / M[i]
                }
                row = k // M[i]
                col = k - row * M[i]
                grid_block_gps_range[current_idx + k] = (
                    ((row * bottom_block_gps_step['lat'] + start_point[0],
                      col * bottom_block_gps_step['lon'] + start_point[1]),
                     ((row + 1) * bottom_block_gps_step['lat'] + start_point[0],
                      (col + 1) * bottom_block_gps_step['lon'] + start_point[1]))
                )

    # calculate the top grid range
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

    # calculate the grid num
    n_grid = 0
    for i in range(C):
        n_grid += M[i] ** 2

    # write to file
    with open(top_grid_path, 'w') as top_grid:
        top_grid.writelines(str(M))
    with open(grid_block_gps_range_path, 'w') as grid_block_range:
        grid_block_range.write(str(grid_block_gps_range) + '\n')
        grid_block_range.write(str(top_grid_block_gps_range) + '\n')

    # map the trajs into the grid
    p = utils.ProgressBar(len(total_trajs), '映射网格轨迹')
    mapped_trajs = []
    for i in range(len(total_trajs)):
        p.update(i)
        mapped_traj = []
        for point in total_trajs[i]:
            # # cal the idx in the top grid
            # C_idx = cal_point_idx(point, _step=top_block_gps_step,
            #                       _base={'lon': gps_range['lon'][0], 'lat': gps_range['lat'][0]})
            #
            # # cal the idx in the bottom grid
            # m = M[C_idx]
            # for j in range(C_idx):
            #     # add the previous bottom grid num.
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
    with open(grid_trajs_path, 'w') as grid_trajs:
        for each_traj in mapped_trajs:
            grid_trajs.writelines(str(each_traj) + '\n')

    # plot the figure
    if is_plot:
        plt.figure(figsize=(6, 5))
        p = utils.ProgressBar(len(total_trajs), '绘制网格轨迹图')
        for i in range(len(total_trajs)):
            p.update(i)
            plt.plot([x[0] for x in total_trajs[i]], [y[1] for y in total_trajs[i]])
            plt.scatter([x[0] for x in total_trajs[i]], [y[1] for y in total_trajs[i]])

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

        plt.xlim(gps_range['lat'][0], gps_range['lat'][1])
        plt.ylim(gps_range['lon'][1], gps_range['lon'][0])
        plt.xlabel('Lat')
        plt.ylabel('Lon')
        ax = plt.gca()
        ax.xaxis.set_ticks_position('top')

        plt.savefig('grid_traj')
        plt.show()

    print('总网格数: %d' % n_grid)

    return n_grid


def cal_split(x_range, y_range, n_split):
    """

    grid split for plot

    Args:
        x_range:
        y_range:
        n_split:

    Returns:
        split_lines:

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
                (x_range[0], y_range[0] + y_range_step * i),
                (x_range[1], y_range[0] + y_range_step * i)
            )]

    return split_lines


def generate_sd_grid_mapping_traj(sd_path, grid_block_gps_range_path, sd_final_path,
                                  mapping_rate=1, mapping_bias=None):
    """

    generate the gird-mapping traj for SD

    Args:
        sd_path                  : input
        grid_block_gps_range_path: input
        sd_final_path            : output
        mapping_rate             :
        mapping_bias             :

    Returns:
        split_lines:

    """

    def random_sampling(grid_range):
        """

        generate a sample point within a grid range

        Args:
            grid_range:

        Returns:
            x:
            y:

        """
        x = np.random.uniform(grid_range[0][0], grid_range[1][0])
        y = np.random.uniform(grid_range[0][1], grid_range[1][1])

        return x, y

    # for pep8
    if mapping_bias is None:
        mapping_bias = {'lat': 0, 'lon': 0}

    with open(sd_path) as sd_file:
        sd = [eval(point) for point in sd_file.readlines()]

    # C = n_top_grid ** 2
    # with open(top_grid_path) as fr_top_grid:
    #     M = eval(fr_top_grid.readline())

    with open(grid_block_gps_range_path) as top_grid_block_gps_range_file:
        fstr = top_grid_block_gps_range_file.readlines()
        grid_block_gps_range = eval(fstr[0])
        # top_grid_block_gps_range = eval(fstr[1])

    reverse_mapped_trajs = []
    for traj in sd:
        reverse_mapped_trajs.append([random_sampling(grid_block_gps_range[i]) for i in traj])

    if not os.path.exists(sd_final_path):
        os.mkdir(sd_final_path)
    # write to files
    fcount = 0
    p = utils.ProgressBar(len(reverse_mapped_trajs), '生成脱敏数据集')

    with open(f'data/{USE_DATA}/trajs_file_name_list.pkl', 'rb') as trajs_file_name_list_file:
        trajs_file_name_list = pickle.loads(trajs_file_name_list_file.read())

    for i in range(len(trajs_file_name_list)):
        p.update(i)

        with open(sd_final_path + f'/{trajs_file_name_list[i]}.txt', 'w') as fw_traj:
            for point in reverse_mapped_trajs[i]:
                # mapping
                point = [point[0] / mapping_rate + mapping_bias['lat'],
                         point[1] / mapping_rate + mapping_bias['lon']]
                fw_traj.write(str(point[0]) + ',' + str(point[1]) + '\n')
            fcount += 1


if __name__ == '__main__':
    epsilon = 0.1
    generate_adaptive_grid('../data/Geolife Trajectories 1.3/MDL/',
                           f'../data/Geolife Trajectories 1.3/Middleware/top_grid_epsilon_{epsilon}.txt',
                           f'../data/Geolife Trajectories 1.3/Middleware/grid_trajs_epsilon_{epsilon}.txt',
                           f'../data/Geolife Trajectories 1.3/Middleware/grid_block_gps_range_epsilon_{epsilon}.txt',
                           1 / 9 * epsilon, epsilon, {'lat': (0, 2640), 'lon': (0, 2040)},
                           n_top_grid=7, add_noise=True, is_plot=False, beta_factor=80)

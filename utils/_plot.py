"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris
# @File    : _plot.py
# @Software: PyCharm
-------------------------------------
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from tqdm import tqdm

from config import *
from utils import ProgressBar

plt.rcParams['savefig.dpi'] = 600
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False
colors = plt.cm.viridis(np.linspace(0, 1, 10))


def plot_scatter(points, traj_type=None, epsilon=None, fig_size=(6, 6), color='black', size=3):
    """

    plot the points

    Args:
        points   : points of trajectories
                   an example [[23.14811, 113.30516],
                               [23.14902, 113.30486]]
        traj_type: trajectories type
        fig_size : figure size
        color    : point color
        size     : point size
        epsilon  : point size

    Returns:
        None

    use example:
        file_list = os.listdir(f'../data/{USE_DATA}/Trajectories/')
        point_list = []
        for file in tqdm(file_list):
            with open(f'../data/{USE_DATA}/Trajectories/' + file, 'r', encoding='utf-8') as traj_file:
                for i in traj_file.readlines():
                    point_list.append(list(map(lambda x: float(x.strip()), i.split(','))))
        plot_scatter(point_list, 'raw')

    """
    plt.figure(figsize=fig_size)
    plt.xlim(21.1, 26.1)
    plt.ylim(109.8, 115.2)
    plt.scatter(x=[p[0] for p in points], y=[p[1] for p in points], color=color, s=size)
    plt.xlabel('latitude')
    plt.ylabel('longitude')
    plt.ylabel('longitude')
    if not os.path.exists('trajs_visualization'):
        os.mkdir('trajs_visualization')
    if traj_type == 'raw':
        plt.savefig(f'trajs_visualization/{USE_DATA}_Trajectories.png')
    else:
        plt.savefig(f'trajs_visualization/{USE_DATA}_{epsilon}.png')
    plt.show()


def plot_trajs(trajs, fig_size=(6, 6), color="mediumpurple", size=5, title='', is_plot_line=False,
               od_only=False, offset=None):
    """

    plot the trajs

    Args:
        trajs       : points of trajectories
        fig_size    : figure size
        color       : point color
        size        : point size
        title       :
        is_plot_line:
        od_only     :
        offset      :

    Returns:
        None

    """
    if offset is None:
        offset = [0, 0]
    p = ProgressBar(len(trajs), 'draw a trajectory graph')
    plt.figure(figsize=fig_size)
    for i in range(len(trajs)):
        p.update(i)
        traj = np.array(trajs[i])
        if od_only:
            traj = [traj[0], traj[-1]]
        x = [x[0] + np.random.uniform(-offset[0], offset[0]) for x in traj]
        y = [y[1] + np.random.uniform(-offset[1], offset[1]) for y in traj]

        if od_only:
            if is_plot_line:
                plt.plot(x[0], y[0], c=color)
                plt.plot(x[1], y[1], c="yellowgreen")
            plt.scatter(x[0], y[0], c=color, s=size)
            plt.scatter(x[1], y[1], c="yellowgreen", s=size)
        else:
            if is_plot_line:
                plt.plot(x, y, c=color)
            plt.scatter(x, y, c=color, s=size)
    plt.title(title)
    plt.show()


def line_chart(dp_stp_list: list, dp_star_list: list, metric: str):
    """

    draw a line chart

    Args:
        dp_stp_list:
        dp_star_list:
        metric:

    Returns:
        None

    use example:
        re_1 = [0.123, 0.234, 0.345, 0.456]
        re_2 = [0.321, 0.432, 0.543, 0.654]
        line_chart(re_1, re_2, 'RE')

    """
    x = [0.1, 0.5, 1.0, 2.0]

    plt.plot(x, dp_stp_list, marker='*', ms=10, label='DP-STP')
    plt.plot(x, dp_star_list, marker='o', mec='r', mfc='w', label='DP-Star')

    plt.legend()
    plt.xticks(x, rotation=1)

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel(r'$\varepsilon$')
    plt.ylabel(metric)

    plt.show()


def three_dimension_piece(data, z_label):
    """

    draw a three dimension piece

    Args:
        data   :
        z_label:

    Returns:
        None

    use example:
        # test data for drawing
        data_ = {'0.1': {'DP-STP': [0.246, 0.468, 0.680], 'DP-Star': [0.111, 0.222, 0.333]},
                 '0.5': {'DP-STP': [0.123, 0.223, 0.324], 'DP-Star': [0.224, 0.234, 0.234]},
                 '1.0': {'DP-STP': [0.135, 0.357, 0.579], 'DP-Star': [0.357, 0.579, 0.791]},
                 '2.0': {'DP-STP': [0.123, 0.456, 0.789], 'DP-Star': [0.002, 0.003, 0.004]}
                 }
        three_dimension_piece(data_, 'RE')

    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    alphas = [0.5, 0.6, 0.8, 0.9]
    y_ticks_labels = [str(i) for i in [0.1, 0.5, 1.0, 2.0]]
    y_ticks = [index + 0.2 for index in range(len(y_ticks_labels))]

    x_ticks_labels = ['GL', 'BK', 'GT']
    x = np.arange(len(x_ticks_labels))  # the label locations
    width = 0.1  # the width of the bars

    # epsilon 0.1 to 2.0
    for a, c, k, yl in zip(alphas, colors, y_ticks, y_ticks_labels):
        ax.bar(x - width / 2, data[yl]['DP-STP'], width=width, zs=k, zdir='y', color=colors[2],
               alpha=a)
        ax.bar(x + width / 2, data[yl]['DP-Star'], width=width, zs=k, zdir='y', color=colors[8],
               alpha=a)

    ax.view_init(elev=20, azim=-130)
    ax.set_box_aspect(aspect=(3, 2, 1.8))

    ax.set_xticks(x)
    ax.set_xticklabels(x_ticks_labels)

    ax.set_ylabel(r'$\varepsilon$')
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks_labels)

    ax.set_zlabel(z_label)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.05f'))

    # On the y axis let's only label the discrete values that we have data for.
    ax.set_yticks(y_ticks)
    if not os.path.exists('three_dimension'):
        os.mkdir('three_dimension')
    filename = f"three_dimension/{z_label}_piece.eps"

    plt.savefig(filename, bbox_inches='tight', pad_inches=0, format='eps')

    plt.show()


def three_dimension_bar(data, metric):
    """

    draw a three dimension bar

    Args:
        data   :
        metric :

    Returns:
        None

    use example:
        data_ = {'0.1': {'Geolife': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'Brinkhoff': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'GZTaxi': {'DP-STP': 0.0, 'DP-Star': 0.0}
                         },
                 '0.5': {'Geolife': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'Brinkhoff': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'GZTaxi': {'DP-STP': 0.0, 'DP-Star': 0.0}
                         },
                 '1.0': {'Geolife': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'Brinkhoff': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'GZTaxi': {'DP-STP': 0.0, 'DP-Star': 0.0}
                         },
                 '2.0': {'Geolife': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'Brinkhoff': {'DP-STP': 0.0, 'DP-Star': 0.0},
                         'GZTaxi': {'DP-STP': 0.0, 'DP-Star': 0.0}
                         }
                 }
        three_dimension_bar(data_, 'TE')

    """
    # setup the figure and axes
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111, projection='3d')

    z_label = metric
    ax1.view_init(elev=19, azim=117)

    width = depth = 0.3

    yticks_labels = ['Geolife', 'Brinkhoff', 'GZTaxi']
    yticks = np.arange(len(yticks_labels)) + depth / 2  # the label locations
    xticks_labels = [str(i) for i in [0.1, 0.5, 1.0, 2.0]]
    xticks = [index + width / 2 for index in range(len(xticks_labels))]

    xticks_dict = dict(zip(xticks_labels, xticks))
    yticks_dict = dict(zip(yticks_labels, yticks))

    _x = np.array(xticks)
    _y = np.array(yticks)
    _xx, _yy = np.meshgrid(_x, _y)

    x, y = _xx.ravel(), _yy.ravel()

    top = x + y
    bottom = np.zeros_like(top)
    # if metric == 'KT':
    #     Z = np.zeros((3, 4))
    #     ax1.plot_surface(_xx, _yy, Z, color='pink', alpha=0.6)
    for each_epsilon in data.keys():
        for each_dataset in data[each_epsilon]:
            index_ = np.where((x == xticks_dict[each_epsilon]) & (y == yticks_dict[each_dataset]))
            x_tmp = x[index_]
            y_tmp = y[index_]
            # DP-STP
            top_stp = data[each_epsilon][each_dataset]["DP-STP"]
            ax1.bar3d(x_tmp - width / 2, y_tmp - depth / 2, bottom, width / 2, depth,
                      [top_stp] * len(x_tmp), shade=True, color=colors[8])

            # DP-Star
            top_star = data[each_epsilon][each_dataset]["DP-Star"]
            ax1.bar3d(x_tmp, y_tmp - depth / 2, bottom, width / 2, depth, top_star,
                      shade=True,
                      color=colors[2])

    ax1.set_box_aspect(aspect=(3, 2, 2))

    ax1.set_ylabel(r'Dataset')
    ax1.set_yticks(yticks)
    ax1.set_yticklabels(yticks_labels)

    ax1.set_zlabel(z_label)
    ax1.zaxis.set_major_formatter(FormatStrFormatter('%.05f'))

    ax1.set_xlabel(r'$\varepsilon$')
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticks_labels)

    if not os.path.exists('three_dimension'):
        os.mkdir('three_dimension')

    plt.savefig(f"three_dimension/{metric}_bar.pdf", bbox_inches='tight', pad_inches=0)
    plt.savefig(f"three_dimension/{metric}_bar.eps", bbox_inches='tight', pad_inches=0)

    plt.show()


if __name__ == '__main__':
    # file_list = os.listdir(f'../data/{USE_DATA}/Trajectories/')
    file_list = os.listdir(f'../data/{USE_DATA}/SD/sd_final_epsilon_0.1/')
    # file_list = os.listdir(f'../data/{USE_DATA}/SD/sd_final_epsilon_0.5/')
    # file_list = os.listdir(f'../data/{USE_DATA}/SD/sd_final_epsilon_1.0/')
    # file_list = os.listdir(f'../data/{USE_DATA}/SD/sd_final_epsilon_2.0/')

    point_list = []
    for file in tqdm(file_list):
        with open(f'../data/{USE_DATA}/SD/sd_final_epsilon_0.1/' + file, 'r', encoding='utf-8') as traj_file:
            for i in traj_file.readlines():
                point_list.append(list(map(lambda x: float(x.strip()), i.split(','))))

    plot_scatter(point_list)

#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""
    the functions for plot.
"""
from __future__ import (absolute_import, unicode_literals)
import matplotlib.pyplot as plt
from utils import ProgressBar


def plot_scatter(points, fig_size=(6, 6), color='purple', size=5):
    """plot the points
    """
    plt.figure(figsize=fig_size)
    plt.scatter(x=[p[0] for p in points], y=[p[1] for p in points], color=color, s=size)
    plt.show()


def plot_traj(trajs, fig_size=(6, 6), color='purple', size=5, is_plot_line=False, od_only=False):
    """plot the traj
    """
    p = ProgressBar(len(trajs), '绘制轨迹图')
    plt.figure(figsize=fig_size)
    for i in range(len(trajs)):
        p.update(i)
        traj = trajs[i]
        if od_only:
            traj = [traj[0], traj[-1]]
        if is_plot_line:
            plt.plot([x[0] for x in traj], [y[1] for y in traj], color=color)
        plt.scatter([x[0] for x in traj], [y[1] for y in traj], color=color, s=size)
    plt.show()

"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : QG
# @File    : trip_error.py
# @Software: PyCharm
-------------------------------------
"""

import os
import pickle

import numpy as np
from joblib import Parallel
from joblib import delayed

from config import *
from metrics import jsd

with open(f'../data/{USE_DATA}/GPS_trajs_range.pkl', 'rb') as GPS_trajs_range_file:
    GPS_trajs_range = pickle.loads(GPS_trajs_range_file.read())

n_grid = 2

lat_len_gps = (GPS_trajs_range[0][1] - GPS_trajs_range[0][0]) / n_grid
lon_len_gps = (GPS_trajs_range[1][1] - GPS_trajs_range[1][0]) / n_grid
A = n_grid ** 2


def calculate_te(epsilon):
    RD = np.zeros((n_grid ** 2) * (n_grid ** 2))
    RSD = np.zeros((n_grid ** 2) * (n_grid ** 2))
    D = []
    SD = []

    files_list = os.listdir(f'../data/{USE_DATA}/Trajectories/')

    for path in files_list:
        with open(f'../data/{USE_DATA}/Trajectories/' + path, 'r') as traj_file:
            T = []

            for line in traj_file.readlines():
                lat_lon = tuple(map(float, line.strip().split(',')))

                lat = int((lat_lon[0] - MIN_LAT_LON[USE_DATA][0]) / lat_len_gps)
                if lat == n_grid:
                    lat -= 1

                lon = int((lat_lon[1] - MIN_LAT_LON[USE_DATA][1]) / lon_len_gps)
                if lon == n_grid:
                    lon -= 1

                T.append(lat * n_grid + lon)

            D.append(T)
            RD[T[0] * A + T[-1]] += 1

    sd_files_list = os.listdir(f"../data/{USE_DATA}/SD/sd_final_epsilon_{epsilon}")

    for path in sd_files_list:
        with open(f"../data/{USE_DATA}/SD/sd_final_epsilon_{epsilon}/" + path, 'r') as traj_file:
            T = []

            for line in traj_file.readlines():
                lat_lon = tuple(map(float, line.strip().split(',')))
                lat = int((lat_lon[0] - MIN_LAT_LON[USE_DATA][0]) / lat_len_gps)
                lon = int((lat_lon[1] - MIN_LAT_LON[USE_DATA][1]) / lon_len_gps)
                if lat * n_grid + lon < A:
                    T.append(lat * n_grid + lon)
            if T:
                SD.append(T)
                try:
                    RSD[T[0] * A + T[-1]] += 1
                except Exception as e:
                    print(e)
                    continue

    RD = RD / np.sum(RD)
    RSD = RSD / np.sum(RSD)

    RD = RD.tolist()
    RSD = RSD.tolist()

    print('epsilon: ', epsilon, 'Trip Error: ', jsd(RD, RSD))


if __name__ == '__main__':
    Parallel(n_jobs=4)(delayed(calculate_te)(i) for i in epsilon_list)

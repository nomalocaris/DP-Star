"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  :
             nomalocaris
             Giyn
# @File    : config.py
# @Software: PyCharm
-------------------------------------
"""

# budget allocation
import os
import pickle

epsilon_alloc = {
    'ag': (1/9),  # adaptive Grid Construction
    'td': (3/9),  # trip distribution extraction
    'markov': (4/9),  # mobility model construction
    'mle': (1/9)  # route length estimation(a median length estimation method)
}

# the number of the top grid
n_top_grid = 7

# a significant parm for adaptive grid, the smaller it is, the more bottom grid will be generate.
beta_factor = 80

epsilon_list = [0.1, 0.5, 1.0, 2.0]

DATASET_LIST = ['Geolife Trajectories 1.3',
                'Brinkhoff',
                'Guangzhou Taxi_30_six_hours',
                'Guangzhou Taxi_60_six_hours'
                ]

MIN_LAT_LON = {'Geolife Trajectories 1.3': [39.4, 115.7],
               'Brinkhoff': [6.558, 0.468],
               'Guangzhou Taxi_30_six_hours': [21.2554, 110.0],
               'Guangzhou Taxi_60_six_hours': [21.2554, 110.0]
               }

MDL_SCALING_RATE = {'Geolife Trajectories 1.3': 1100,
                    'Brinkhoff': 300,
                    'Guangzhou Taxi_30_six_hours': 500,
                    'Guangzhou Taxi_60_six_hours': 500
                    }

TRAJS_NUM = {'Geolife Trajectories 1.3': 14650,
             'Brinkhoff': 50000,
             'Guangzhou Taxi_30_six_hours': 30000,
             'Guangzhou Taxi_60_six_hours': 30000,
             }

USE_DATA = DATASET_LIST[2]

with open(f'../data/{USE_DATA}/MDL_trajs_range.pkl', 'rb') as MDL_trajs_range_file:
    MDL_trajs_range = pickle.loads(MDL_trajs_range_file.read())

with open(f'../data/{USE_DATA}/GPS_trajs_range.pkl', 'rb') as GPS_trajs_range_file:
    GPS_trajs_range = pickle.loads(GPS_trajs_range_file.read())

gps_range = {'lat': tuple(MDL_trajs_range[0]), 'lon': tuple(MDL_trajs_range[1])}
mapping_bias = {'lat': GPS_trajs_range[0][0], 'lon': GPS_trajs_range[1][0]}

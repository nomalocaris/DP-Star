"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : QG
# @File    : _traj.py
# @Software: PyCharm
-------------------------------------
"""

import pickle

from joblib import Parallel
from joblib import delayed
from tqdm import tqdm
from config import *
from utils import *


def trajs_range(trajs_path, dtype='common'):
    """

    calculate the latitude and longitude range of the trajectory

    """
    traj_files = os.listdir(trajs_path)
    trajs_num = len(traj_files)

    print('number of trajectories: ', trajs_num)

    if dtype == 'common':
        min_lon, min_lat = np.inf, np.inf
        max_lon, max_lat = -np.inf, -np.inf
    else:
        min_lon, min_lat = 180, 90
        max_lon, max_lat = -180, -90

    p = ProgressBar(trajs_num, 'Calculate the latitude and longitude range')
    for i in range(trajs_num):
        p.update(i)
        traj_file = traj_files[i]
        with open(trajs_path + traj_file) as file:
            for line in file.readlines():
                pos = eval(line)
                min_lat = pos[0] if pos[0] < min_lat else min_lat
                max_lat = pos[0] if pos[0] > max_lat else max_lat
                min_lon = pos[1] if pos[1] < min_lon else min_lon
                max_lon = pos[1] if pos[1] > max_lon else max_lon

    return [min_lat, max_lat], [min_lon, max_lon]


def process_mdl_trajs_data(mdl_trajs_path: str, frontend_data_path: str, traj_files_list: str,
                           rate: int, min_latitude: float, min_longitude: float):
    if not os.path.exists(frontend_data_path.split('MDL')[0]):
        os.mkdir(frontend_data_path.split('MDL')[0])
    if not os.path.exists(frontend_data_path):
        os.mkdir(frontend_data_path)

    for traj_path in traj_files_list:
        processed_data = []
        with open(mdl_trajs_path + traj_path, 'r') as traj_file:
            for line in traj_file.readlines():
                point_tuple = eval(line)
                point_list = [(point_tuple[1] / rate) + min_longitude,
                              (point_tuple[0] / rate) + min_latitude]
                processed_data.append(point_list)

        with open(frontend_data_path + traj_path, 'w') as front_mdl_file:
            front_mdl_file.writelines(str(processed_data))


def process_final_trajs_data(sd_final_file_path: str, file_name_list: list, processed_path: str):
    if not os.path.exists(processed_path.split('SD')[0]):
        os.mkdir(processed_path.split('SD')[0])
    if not os.path.exists(processed_path.split('sd_final')[0]):
        os.mkdir(processed_path.split('sd_final')[0])
    if not os.path.exists(processed_path):
        os.mkdir(processed_path)

    trajs_len = len(file_name_list)

    for i in range(trajs_len):
        with open(sd_final_file_path + "/" + file_name_list[i], 'r') as sd_final_file:
            sd_final_trajs_list = sd_final_file.readlines()

        processed_data = []
        for point in sd_final_trajs_list:
            processed_data.append(list(map(float, list(reversed(point.split(', '))))))

        with open(processed_path + file_name_list[i], 'w') as processed_file:
            processed_file.writelines(str(processed_data))


def scaling_trajs_data(src_path, out_path):
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    file_list = [f'{i}.plt' for i in range(1, 50001)]
    for file in file_list:
        with open(src_path + file, 'r') as traj_file:
            with open(out_path + file, 'w') as scaled_traj_file:
                for line in traj_file.readlines():
                    # (lng, lat)
                    point_tuple = eval(line)
                    # lat, lng
                    scaled_traj_file.writelines(f'{point_tuple[1] / 600}, {point_tuple[0] / 600}\n')


def swap_lon_lat(src_path, out_path):
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    for traj_file in tqdm(src_path):
        with open(f'../data/{USE_DATA}/Data/' + traj_file, 'r') as lon_lat_file:
            with open(out_path + traj_file, 'w') as lat_lon_file:
                last_point = [0, 0]
                for line in lon_lat_file.readlines():
                    point = list(map(float, line.strip().split(',')))
                    # clean dirty data
                    if last_point == point:
                        continue
                    last_point = point
                    if (point[0] < 110) or (point[0] > 115) or (point[1] < 20) or (point[1] > 25):
                        continue
                    else:
                        lat_lon_file.writelines(str(point[1]) + ', ' + str(point[0]) + '\n')


if __name__ == '__main__':
    """calculate trajectory range"""
    # GPS_trajs_range = trajs_range(f'../data/{USE_DATA}/Trajectories/')
    # with open(f'../data/{USE_DATA}/GPS_trajs_range.pkl', 'wb') as GPS_trajs_range_file:
    #     GPS_trajs_range_str = pickle.dumps(GPS_trajs_range)
    #     GPS_trajs_range_file.write(GPS_trajs_range_str)

    # with open(f'../data/{USE_DATA}/GPS_trajs_range.pkl', 'rb') as GPS_trajs_range_file:
    #     GPS_trajs_range = pickle.loads(GPS_trajs_range_file.read())
    # print(GPS_trajs_range)

    # MDL_trajs_range = trajs_range(f'../data/{USE_DATA}/MDL/')
    # with open(f'../data/{USE_DATA}/MDL_trajs_range.pkl', 'wb') as MDL_trajs_range_file:
    #     MDL_trajs_range_str = pickle.dumps(MDL_trajs_range)
    #     MDL_trajs_range_file.write(MDL_trajs_range_str)
    #
    # with open(f'../data/{USE_DATA}/MDL_trajs_range.pkl', 'rb') as MDL_trajs_range_file:
    #     MDL_trajs_range = pickle.loads(MDL_trajs_range_file.read())
    # print(MDL_trajs_range)

    """process trajectory data according to the required interface of the front end"""
    # mdl_traj_files = os.listdir(f'../data/{USE_DATA}/MDL/')
    # task_list = list(equally_divide_list(mdl_traj_files, 6))
    # Parallel(n_jobs=6)(delayed(process_mdl_trajs_data)(f'../data/{USE_DATA}/MDL/',
    #                                                    f'../data/{USE_DATA}/FrontEndData/MDL/',
    #                                                    i, MDL_SCALING_RATE[USE_DATA],
    #                                                    MIN_LAT_LON[USE_DATA][0],
    #                                                    MIN_LAT_LON[USE_DATA][1]) for i in task_list)

    # with open(f'../data/{USE_DATA}/trajs_file_name_list.pkl', 'rb') as trajs_file_name_list_file:
    #     trajs_file_name_list = pickle.loads(trajs_file_name_list_file.read())
    #
    # sd_file_dir = f'../data/{USE_DATA}/SD/'
    # sd_file_list = list(filter(lambda x: 'final' in x, os.listdir(sd_file_dir)))
    #
    # save_path = '../data/{}/FrontEndData/SD/{}/'
    #
    # Parallel(n_jobs=4)(delayed(process_final_trajs_data)(sd_file_dir + i,
    #                                                      trajs_file_name_list,
    #                                                      save_path.format(USE_DATA, i)) for i in sd_file_list)

    """save the trajectory file name to pkl"""
    # trajs_file_name_list = os.listdir(f'../data/{USE_DATA}/MDL/') if not USE_DATA == 'Brinkhoff' else [f'{i}.txt' for i in range(1, 50001)]
    #
    # with open(f'../data/{USE_DATA}/trajs_file_name_list.pkl', 'wb') as trajs_file_name_list_file:
    #     trajs_file_name_list_str = pickle.dumps(trajs_file_name_list)
    #     trajs_file_name_list_file.write(trajs_file_name_list_str)
    #
    # with open(f'../data/{USE_DATA}/trajs_file_name_list.pkl', 'rb') as trajs_file_name_list_file:
    #     trajs_file_name_list = pickle.loads(trajs_file_name_list_file.read())

    """scale the brinkhoff dataset"""
    # scaling_trajs_data('../data/Brinkhoff/Data/', '../data/Brinkhoff/Trajectories/')

    """exchange the latitude and longitude position of Guangzhou taxi data"""
    # raw_traj_files = os.listdir(f'../data/{USE_DATA}/Data/')
    # task_list = list(equally_divide_list(raw_traj_files, 7))
    #
    # Parallel(n_jobs=7)(delayed(swap_lon_lat)(i, f'../data/{USE_DATA}/Trajectories/'
    #                                          ) for i in task_list)

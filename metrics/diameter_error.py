"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : QG
# @File    : diameter_error.py
# @Software: PyCharm
-------------------------------------
"""

from joblib import Parallel
from joblib import delayed

from config import *
from metrics import *


def _cal_diameter_error(d_max_len, d_max_len_arr, sd_max_len, sd_max_len_arr):
    """

    calculate diameter error(DE)

    Args:
        d_max_len     :
        d_max_len_arr :
        sd_max_len    :
        sd_max_len_arr:

    Returns:

    """
    ep_D = [0 for _ in range(20)]
    ep_SD = [0 for _ in range(20)]
    for item in d_max_len_arr:
        num = int(item / (d_max_len / 20))
        if num < 20:
            ep_D[num] += 1
        else:
            ep_D[19] += 1

    for item in sd_max_len_arr:
        num = int(item / (sd_max_len / 20))
        if num < 20:
            ep_SD[num] += 1
        else:
            ep_SD[19] += 1

    ep_D = np.array(ep_D, dtype='float32')
    ep_D /= np.sum(ep_D)
    ep_D = ep_D.tolist()
    ep_SD = np.array(ep_SD, dtype='float32')
    ep_SD /= np.sum(ep_SD)
    ep_SD = ep_SD.tolist()
    diameter_error = jsd(ep_D, ep_SD)

    return diameter_error


def cal_diameter_error(d_path, sd_path):
    """

    calculate diameter error(DE) (main function)

    Args:
        d_path :
        sd_path:

    Returns:

    """
    diameter, diameter_array = d_len(d_path)

    if not os.path.exists(USE_DATA):
        os.mkdir(USE_DATA)

    with open(f"{USE_DATA}/diameter_array.txt", "r") as output:
        diameter_array = eval(output.read())
    s_diameter, s_diameter_array = d_len(sd_path)

    diameter_error_ = _cal_diameter_error(diameter, diameter_array, s_diameter, s_diameter_array)

    print('Diameter Error: ', sd_path, diameter_error_)

    return diameter_error_


def count_d_path(d_path):
    """

    calculate trajectory path

    Args:
        d_path :

    Returns:

    """
    diameter_array = d_len(d_path)[1]

    if not os.path.exists(USE_DATA):
        os.mkdir(USE_DATA)
    with open(f"{USE_DATA}/diameter_array.txt", "w") as output:
        output.write(str(diameter_array))


if __name__ == '__main__':
    count_d_path(f"../data/{USE_DATA}/Trajectories/")
    Parallel(n_jobs=4)(delayed(cal_diameter_error)(f"../data/{USE_DATA}/Trajectories/",
                                                   f"../data/{USE_DATA}/SD/sd_final_epsilon_{i}/"
                                                   ) for i in epsilon_list)

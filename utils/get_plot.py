"""
-------------------------------------
# -*- coding: utf-8 -*-
# @Author  : nomalocaris
# @File    : get_plot.py
# @Software: PyCharm
-------------------------------------
"""

import os

import matplotlib.pyplot as plt

plt.rc('font', family='Times New Roman', size=25)


def get_metrics(d_2: list, d_3: list, d_4: list, d_5: list, d_6: list, metric: str):
    x = [1, 2, 3, 4]
    x_ = ['0.1', '0.5', '1.0', '2.0']
    plt.figure(figsize=(10.5, 7.6))
    plt.plot(x, d_2, marker='*', label='d=2', ms=10)
    plt.plot(x, d_3, marker='o', label='d=3', ms=10)
    plt.plot(x, d_4, marker='x', label='d=4', ms=10)
    plt.plot(x, d_5, marker='+', label='d=5', ms=10)
    plt.plot(x, d_6, marker='v', label='d=6', ms=10)

    plt.legend()  # 让图例生效
    plt.xticks(x, x_)

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel(r'$\varepsilon$')  # X轴标签
    plt.ylabel(metric)  # Y轴标签
    if not os.path.exists('d_parameter'):
        os.mkdir('d_parameter')
    plt.savefig(f'd_parameter/{metric}.pdf', pad_inches=0.01)
    plt.savefig(f'd_parameter/{metric}.eps', pad_inches=0.01)
    plt.show()


def get_metrics_direction(d_2: list, d_3: list, d_4: list, metric: str):
    x = [1, 2, 3, 4]
    x_ = ['0.1', '0.5', '1.0', '2.0']

    plt.figure(figsize=(12, 7.6))

    plt.plot(x, d_2, marker='*', label='<α,γ>')
    plt.plot(x, d_3, marker='o', label='30°')
    plt.plot(x, d_4, marker='x', label='60°')

    plt.legend()  # 让图例生效
    plt.xticks(x, x_)

    plt.xlabel(r'$\varepsilon$')  # X轴标签
    plt.ylabel(metric)  # Y轴标签

    if not os.path.exists('direction_parameter'):
        os.mkdir('direction_parameter')
    plt.savefig(f'direction_parameter/{metric}.pdf', pad_inches=0.01)
    plt.savefig(f'direction_parameter/{metric}.eps', pad_inches=0.01)
    plt.show()


def get_metrics_density(g_6: list, g_12: list, g_18: list, metric: str):
    x = [1, 2, 3, 4]
    x_ = ['0.1', '0.5', '1.0', '2.0']

    plt.figure(figsize=(12, 7.6))

    plt.plot(x, g_6, marker='*', label='6×6')
    plt.plot(x, g_12, marker='o', label='12×12')
    plt.plot(x, g_18, marker='x', label='18×18')

    plt.legend()  # 让图例生效
    plt.xticks(x, x_)

    plt.xlabel(r'$\varepsilon$')  # X轴标签
    plt.ylabel(metric)  # Y轴标签

    if not os.path.exists('density_parameter'):
        os.mkdir('density_parameter')
    plt.savefig(f'density_parameter/{metric}.pdf', pad_inches=0.01)
    plt.savefig(f'density_parameter/{metric}.eps', pad_inches=0.01)
    plt.show()


if __name__ == '__main__':
    # guangzhou_taxi_30_stp_qa_d2 = [0.0005, 0.0002, 0.0004, 0.0002]
    # guangzhou_taxi_30_stp_qa_d3 = [0.0013, 0.0126, 0.0250, 0.0066]
    # guangzhou_taxi_30_stp_qa_d4 = [0.0004, 0.0056, 0.0083, 0.0003]
    # guangzhou_taxi_30_stp_qa_d5 = [0.0043, 0.0123, 0.0020, 0.0006]
    # guangzhou_taxi_30_stp_qa_d6 = [0.0033, 0.0023, 0.1059, 0.0036]
    #
    # get_metrics(guangzhou_taxi_30_stp_qa_d2, guangzhou_taxi_30_stp_qa_d3,
    #             guangzhou_taxi_30_stp_qa_d4, guangzhou_taxi_30_stp_qa_d5,
    #             guangzhou_taxi_30_stp_qa_d6, 'RE')
    #
    # guangzhou_taxi_30_stp_fps_d2 = [0.502, 0.525, 0.581, 0.625]
    # guangzhou_taxi_30_stp_fps_d3 = [0.173, 0.466, 0.583, 0.593]
    # guangzhou_taxi_30_stp_fps_d4 = [0.259, 0.528, 0.592, 0.722]
    # guangzhou_taxi_30_stp_fps_d5 = [0.557, 0.679, 0.774, 0.912]
    # guangzhou_taxi_30_stp_fps_d6 = [0.039, 0.418, 0.592, 0.591]
    #
    # get_metrics(guangzhou_taxi_30_stp_fps_d2, guangzhou_taxi_30_stp_fps_d3,
    #             guangzhou_taxi_30_stp_fps_d4, guangzhou_taxi_30_stp_fps_d5,
    #             guangzhou_taxi_30_stp_fps_d6, 'FPS')
    #
    # guangzhou_taxi_30_stp_kt_d2 = [0.002, 0.003, 0.006, 0.020]
    # guangzhou_taxi_30_stp_kt_d3 = [-0.0008, 0.03, 0.087, 0.080]
    # guangzhou_taxi_30_stp_kt_d4 = [-0.021, 0.057, 0.132, 0.139]
    # guangzhou_taxi_30_stp_kt_d5 = [-0.004, 0.130, 0.151, 0.172]
    # guangzhou_taxi_30_stp_kt_d6 = [0.003, 0.008, 0.116, 0.097]
    #
    # get_metrics(guangzhou_taxi_30_stp_kt_d2, guangzhou_taxi_30_stp_kt_d3,
    #             guangzhou_taxi_30_stp_kt_d4, guangzhou_taxi_30_stp_kt_d5,
    #             guangzhou_taxi_30_stp_kt_d6, 'KT')
    #
    # guangzhou_taxi_30_stp_te_d2 = [0.007, 0.006, 0.005, 0.003]
    # guangzhou_taxi_30_stp_te_d3 = [0.246, 0.226, 0.197, 0.163]
    # guangzhou_taxi_30_stp_te_d4 = [0.166, 0.073, 0.046, 0.030]
    # guangzhou_taxi_30_stp_te_d5 = [0.131, 0.056, 0.042, 0.035]
    # guangzhou_taxi_30_stp_te_d6 = [0.101, 0.074, 0.191, 0.051]
    #
    # get_metrics(guangzhou_taxi_30_stp_te_d2, guangzhou_taxi_30_stp_te_d3,
    #             guangzhou_taxi_30_stp_te_d4, guangzhou_taxi_30_stp_te_d5,
    #             guangzhou_taxi_30_stp_te_d6, 'TE')
    #
    # guangzhou_taxi_30_stp_de_d2 = [0.003, 0.017, 0.005, 0.003]
    # guangzhou_taxi_30_stp_de_d3 = [0.041, 0.085, 0.075, 0.077]
    # guangzhou_taxi_30_stp_de_d4 = [0.027, 0.034, 0.052, 0.058]
    # guangzhou_taxi_30_stp_de_d5 = [0.227, 0.221, 0.208, 0.174]
    # guangzhou_taxi_30_stp_de_d6 = [0.191, 0.237, 0.214, 0.189]
    #
    # get_metrics(guangzhou_taxi_30_stp_de_d2, guangzhou_taxi_30_stp_de_d3,
    #             guangzhou_taxi_30_stp_de_d4, guangzhou_taxi_30_stp_de_d5,
    #             guangzhou_taxi_30_stp_de_d6, 'DE')

    """"""

    # guangzhou_taxi_30_stp_qa_ay = [0.0005, 0.0002, 0.0004, 0.0002]
    # guangzhou_taxi_30_stp_qa_30 = [0.0013, 0.0011, 0.0012, 0.0007]
    # guangzhou_taxi_30_stp_qa_60 = [0.0024, 0.0016, 0.0010, 0.0009]
    #
    # get_metrics_direction(guangzhou_taxi_30_stp_qa_ay, guangzhou_taxi_30_stp_qa_30,
    #                       guangzhou_taxi_30_stp_qa_60, 'RE')
    #
    # guangzhou_taxi_30_stp_fps_ay = [0.502, 0.525, 0.581, 0.625]
    # guangzhou_taxi_30_stp_fps_30 = [0.701, 0.613, 0.633, 0.593]
    # guangzhou_taxi_30_stp_fps_60 = [0.648, 0.612, 0.587, 0.652]
    #
    # get_metrics_direction(guangzhou_taxi_30_stp_fps_ay,
    #                       guangzhou_taxi_30_stp_fps_30,
    #                       guangzhou_taxi_30_stp_fps_60, 'FPS')
    #
    # guangzhou_taxi_30_stp_kt_ay = [0.002, 0.003, 0.006, 0.020]
    # guangzhou_taxi_30_stp_kt_30 = [-0.019, 0.0009, 0.0043, 0.0042]
    # guangzhou_taxi_30_stp_kt_60 = [-0.008, 0.0012, 0.0014, 0.0051]
    #
    # get_metrics_direction(guangzhou_taxi_30_stp_kt_ay,
    #                       guangzhou_taxi_30_stp_kt_30,
    #                       guangzhou_taxi_30_stp_kt_60, 'KT')
    #
    # guangzhou_taxi_30_stp_de_ay = [0.003, 0.017, 0.005, 0.003]
    # guangzhou_taxi_30_stp_de_30 = [0.026, 0.019, 0.007, 0.005]
    # guangzhou_taxi_30_stp_de_60 = [0.015, 0.016, 0.005, 0.006]
    #
    # get_metrics_direction(guangzhou_taxi_30_stp_de_ay,
    #                       guangzhou_taxi_30_stp_de_30,
    #                       guangzhou_taxi_30_stp_de_60, 'DE')

    """"""

    guangzhou_taxi_30_stp_re_g6 = [0.027, 0.001, 0.001, 0.011]
    guangzhou_taxi_30_stp_re_g12 = [0.010, 0.004, 0.0006, 0]
    guangzhou_taxi_30_stp_re_g18 = [0.0005, 0.0002, 0.0004, 0.0002]

    get_metrics_density(guangzhou_taxi_30_stp_re_g6, guangzhou_taxi_30_stp_re_g12,
                        guangzhou_taxi_30_stp_re_g18, 'RE')

    guangzhou_taxi_30_stp_fps_g6 = [1.740, 1.872, 1.034, 1.931]
    guangzhou_taxi_30_stp_fps_g12 = [1.725, 1.766, 1.702, 1.869]
    guangzhou_taxi_30_stp_fps_g18 = [0.502, 0.525, 0.581, 0.625]

    get_metrics_density(guangzhou_taxi_30_stp_fps_g6,
                        guangzhou_taxi_30_stp_fps_g12,
                        guangzhou_taxi_30_stp_fps_g18, 'FPS')

    guangzhou_taxi_30_stp_kt_g6 = [0.085, 0.364, 0.320, 0.288]
    guangzhou_taxi_30_stp_kt_g12 = [0.081, 0.317, 0.289, 0.286]
    guangzhou_taxi_30_stp_kt_g18 = [0.002, 0.003, 0.006, 0.020]

    get_metrics_density(guangzhou_taxi_30_stp_kt_g6,
                        guangzhou_taxi_30_stp_kt_g12,
                        guangzhou_taxi_30_stp_kt_g18, 'KT')

    guangzhou_taxi_30_stp_de_g6 = [0.454, 0.519, 0.519, 0.281]
    guangzhou_taxi_30_stp_de_g12 = [0.454, 0.519, 0.519, 0.107]
    guangzhou_taxi_30_stp_de_g18 = [0.003, 0.017, 0.005, 0.003]

    get_metrics_density(guangzhou_taxi_30_stp_de_g6,
                        guangzhou_taxi_30_stp_de_g12,
                        guangzhou_taxi_30_stp_de_g18, 'DE')

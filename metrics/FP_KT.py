import numpy as np
import os

pattern = ['Frequent_Pattern_init.txt', 'Frequent_Pattern_sd.txt']
path_list = ['../../data/Geolife Trajectories 1.3/Trajectories7000/', '../../data/Geolife Trajectories '
                                                                  '1.3/sd/sd_final_MDL1100_ep0.1/', '../../data/Geolife '
                                                                                            'Trajectories '
                                                                                            '1.3/sd/sd_final_MDL1100_ep0.5/',
             '../../data/Geolife Trajectories 1.3/sd/sd_final_MDL1100_ep1.0/', '../../data/Geolife Trajectories '
                                                                       '1.3/sd/sd_final_MDL1100_ep2.0/']
path_test = ['../../data/Geolife Trajectories 1.3/Trajectories/', '../../data/Geolife Trajectories '
                                                                  '1.3/test/0/', '../../data/Geolife '
                                                                                            'Trajectories '
                                                                                            '1.3/test/1/',
             '../../data/Geolife Trajectories 1.3/test/2/', '../../data/Geolife Trajectories '
                                                                       '1.3/test/3/']


def get_Frequent_Pattern(init_path='../../data/Geolife Trajectories 1.3/Trajectories/',
                         min_latitude=39.6,
                         min_longitude=115.8,
                         len_latitude=1.2,
                         len_longitude=1.6, para="init"):
    """
    存储数据的频繁模式
    :param init_path:数据路径
    :param min_latitude:最小纬度
    :param min_longitude:最小经度
    :param len_latitude:纬度差值
    :param len_longitude:经度差值
    :param para:计算频繁模式,选择数据集
    :return:排序好的频繁模式集
    """

    lat_accu = len_latitude / 6  # 维度边的跨度
    lon_accu = len_longitude / 6  # 经度边的跨度

    # 存频繁模式
    Frequent_Pattern = {}

    base_path_list = os.listdir(init_path)
    for path in base_path_list:
        file_object = open(init_path + path, 'r')  # 读取轨迹数据文件
        T0 = []
        now_path_arr = []

        for line in file_object.readlines():
            w = float(line.strip().split(',')[0].strip())
            w = int((w - min_latitude) / lat_accu)  # 维度对应网格的位置
            j = float(line.strip().split(',')[1].strip())
            j = int((j - min_longitude) / lon_accu)  # 经度对应网格的位置

            if len(T0) > 0 and w * 6 + j == T0[-1]:  # 排除连续出现在一个格子里面的情况
                continue
            T0.append(w * 6 + j)  # 格子的编号

        for i in range(len(T0) - 2):
            for j in range(i + 2, len(T0)):
                # if j-i > 5:  # ?
                #     break
                P = tuple(T0[i: j + 1].copy())  # 找频繁模式(至少大于等于三个单元网格)
                if P in Frequent_Pattern.keys():
                    Frequent_Pattern[P] += 1
                else:
                    Frequent_Pattern[P] = 1
    if para == "init":
        f = open(pattern[0], 'w')
    else:
        f = open(pattern[1], 'w')

    for record in Frequent_Pattern.keys():
        f.writelines(str(record) + ':' + str(Frequent_Pattern[record]) + '\n')
    f.close()
    return sorted(Frequent_Pattern.items(), key=lambda x: x[1], reverse=True)


def get_Fredata(para="init"):
    """
    获取频繁模式数据
    :param para:计算频繁模式,选择数据集
    :return:
    """
    if para == "init":
        f = open(pattern[0], 'r')
    else:
        f = open(pattern[1], 'r')

    Fre_dict = {}
    for line in f.readlines():
        Fre_dict[tuple((line.split(':')[0].strip()[1:-1]).split(','))] = int(line.split(':')[1].strip())
    # print(sorted(Fre_dict.items(), key=lambda x: x[1], reverse=True))
    dict_ = {}
    for item in sorted(Fre_dict.items(), key=lambda x: x[1], reverse=True):
        dict_[item[0]] = item[1]
    return dict_


def get_FP(init_dict, sd_dict):
    """
    计算FP指标
    :param init_dict:原始数据的频繁模式字典
    :param sd_dict:生成数据的频繁模式字典
    :return:FP指标
    """
    sum_D = sum(list(init_dict.values()))
    sum_SD = sum(list(sd_dict.values()))
    top_k = list(init_dict.keys())[:50]
    FP = 0
    for index, key in init_dict.items():
        init_dict[index] = key /sum_D

    for index, key in sd_dict.items():
        sd_dict[index] = key /sum_SD
    i = 0
    for p in list(init_dict.keys()):
        if i >= 50:
            break
        if p in sd_dict.keys():
            i += 1
            re = abs(init_dict[p] - sd_dict[p]) / init_dict[p]  # re <= 1
            FP += re
            print(i, init_dict[p], sd_dict[p])
    return FP/50


def get_KT(init_dict, sd_dict):
    """
    计算KT指标
    :param init_dict:原始数据的频繁模式字典
    :param sd_dict:生成数据的频繁模式字典
    :return:KT指标
    """
    # input(type(init_dict))
    # print(init_dict.keys())
    # print(init_dict.values())
    # input(init_dict)
    concor_count = 0
    discor_count = 0
    key_list = list(init_dict.keys())[:50]
    for i in range(len(key_list)-1):
        for j in range(i+1, len(key_list)):
            if (key_list[i] in sd_dict.keys()) and (key_list[j] in sd_dict.keys()):
                if (init_dict[key_list[i]] > init_dict[key_list[j]] and sd_dict[key_list[i]] > sd_dict[key_list[j]]) or \
                        (init_dict[key_list[i]] < init_dict[key_list[j]] and sd_dict[key_list[i]] < sd_dict[key_list[j]]):
                    concor_count += 1
                else:
                    discor_count += 1
    print("KT差值：", (concor_count - discor_count))
    KT = (concor_count - discor_count) / (50 * 49 / 2)
    return KT


if __name__ == '__main__':
    get_Frequent_Pattern(path_list[0],
                               min_latitude=39.6,
                               min_longitude=115.8,
                               len_latitude=1.2,
                               len_longitude=1.6,
                               para="init")
    dict_init = get_Fredata(para="init")
    # with open("FPdict_init.txt", "r") as output:
    #     dict_init = eval(output.read())
    # print(dict_init)
    for i in range(1, 2):
        get_Frequent_Pattern(path_test[i],
                                   min_latitude=39.6,
                                   min_longitude=115.8,
                                   len_latitude=1.2,
                                   len_longitude=1.6,
                                   para="sd")
        dict_sd = get_Fredata(para="sd")
        FP = get_FP(dict_init, dict_sd)
        KT = get_KT(dict_init, dict_sd)
        print(path_test[i], FP, KT)

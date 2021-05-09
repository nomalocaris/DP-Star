import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
import matplotlib.font_manager as fm  # 字体管理器


def run_data():
    data = {
        "Query AvRE": [6.85e-04,8.22e-03,8.15e-02,8.54],
        "Freq Patten AvRE": [0.13,1.08,1.24,1.31],
        "Trip Error": [2.27e-03,4.17e-02,3.67e-01,6.80e-01],
        "Diameter Error": [1.04e-05,4.98e-04,0.27,0.41]
    }
    return data


def get_plot(metrics, data):
    x_data = [0.1, 0.5, 1, 2]
    rage = [str([0.0001, 0.00099]), str([0.001, 0.0099]), str([0.01, 0.099]),  str([0.1, 0.99])]
    paper_data = {
        "Query AvRE": [0.295, 0.203, 0.171, 0.159],
        "Freq Patten AvRE": [0.340, 0.329, 0.322, 0.329],
        "Trip Error": [0.071, 0.054, 0.034, 0.017],
        "Diameter Error": [0.103, 0.089, 0.078, 0.076]
    }
    # 防止乱码
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.plot(rage, data, color="red", marker="*", label="offset")
    # plt.plot(x_data, data, color="red", marker="*", label="geolife")
    # plt.plot(x_data, paper_data[metrics], color="blue", marker="o", label="paper")
    plt.ylabel("指标结果")
    plt.title(metrics)
    plt.legend()
    plt.savefig('../data/Geolife Trajectories 1.3/' + metrics + ".jpg")
    plt.show()


if __name__ == '__main__':
    for index, key in run_data().items():
        get_plot(index, key)

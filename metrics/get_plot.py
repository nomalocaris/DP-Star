import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
import matplotlib.font_manager as fm  # 字体管理器


def run_data():
    data = {
        "Query AvRE": [0.060, 0.046, 0.142, 0.025],
        # "Freq Patten AvRE": [0.748, 0.795, 0.865, 0.827],
        "Trip Error": [0.390, 0.203, 0.182, 0.208]
        # "Diameter Error": [0.455, 0.350, 0.332, 0.318]
    }
    return data


def get_plot(metrics, data):
    x_data = [0.1, 0.5, 1, 2]
    paper_data = {
        "Query AvRE": [0.295, 0.203, 0.171, 0.159],
        "Freq Patten AvRE": [0.340, 0.329, 0.322, 0.329],
        "Trip Error": [0.071, 0.054, 0.034, 0.017],
        "Diameter Error": [0.103, 0.089, 0.078, 0.076]
    }
    # 防止乱码
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.plot(x_data, data, color="red", marker="*", label="geolife")
    plt.plot(x_data, paper_data[metrics], color="blue", marker="o", label="paper")
    plt.ylabel("指标结果")
    plt.title(metrics)
    plt.legend()
    plt.savefig('../data/Geolife Trajectories 1.3/' + metrics + ".jpg")
    plt.show()


if __name__ == '__main__':
    for index, key in run_data().items():
            get_plot(index, key)

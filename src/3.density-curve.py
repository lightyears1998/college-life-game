"""
绘制种群密度曲线的图像
"""

from util import mkdirp
import numpy as np
from matplotlib import pyplot as plt

OUTPUT_DIR = "../out/3.density-curve/"


def plot():
    x = np.arange(0, 1, 0.001)
    y = -(x-1)**2 + 1

    plt.plot(x, y)
    plt.axis([0, 1, 0, 1])
    plt.savefig(OUTPUT_DIR + "density-curve.png")


if __name__ == "__main__":
    mkdirp(OUTPUT_DIR)
    plot()

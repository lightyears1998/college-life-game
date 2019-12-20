"""
氧气的扩散模型

规则：
1. 镜像边界
2. 气体扩散公式
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from util import mkdirp


OUTPUT_DIR = "../out/2.oxygen/"

SIZE = 8
CELLS = [(i, j) for i in range(0, SIZE) for j in range(0, SIZE)]

MAX_ITERATION = 32

initial_oxygen_distribution: pd.DataFrame
distributions: [pd.DataFrame]


def init():
    global initial_oxygen_distribution, distributions

    initial_oxygen_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=float)
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            initial_oxygen_distribution.iat[i, j] = np.random.rand()
    distributions = [initial_oxygen_distribution.copy(), initial_oxygen_distribution.copy()]


def show_oxygen_distribution(ax, board, title=None):
    ax.imshow(board, cmap=plt.cm.Blues, vmin=0, vmax=1)
    ax.set_xticks(np.arange(0, SIZE, 1))
    ax.set_yticks(np.arange(0, SIZE, 1))
    ax.set_xticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_yticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_xticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.grid(which="minor", color='w', linestyle='-', linewidth=2)
    if title:
        ax.title.set_text(title)


def iterate():
    global distributions

    for generation in range(1, MAX_ITERATION + 1):
        current_distribution = distributions[generation % 2]
        last_distribution = distributions[(generation + 1) % 2]

        for cols in current_distribution:
            current_distribution[cols].values[:] = 0

        for i, j in CELLS:
            total = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    ti, tj = (i + dx + SIZE) % SIZE, (j + dy + SIZE) % SIZE
                    total = total + (1 - min(1, last_distribution.iat[ti, tj]))
            total = total - (1 - min(1, last_distribution.iat[i, j]))
            if total > 0:  # 当周边存在格子氧气密度小于1时进行扩散
                diffusion_oxygen = last_distribution.iat[i, j] / 2  # 散发当前格子氧气浓度的一半\
                total_shared = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        ti, tj = (i + dx + SIZE) % SIZE, (j + dy + SIZE) % SIZE
                        target_cell = last_distribution.iat[ti, tj]
                        shared_oxygen = diffusion_oxygen * ((1 - min(1, target_cell)) / total)
                        total_shared = total_shared + shared_oxygen
                        current_distribution.iat[ti, tj] = current_distribution.iat[ti, tj] + shared_oxygen
                # 为避免浮点误差，不应该简单地取当前格子氧气浓度的一半，而是上次的氧气浓度减去当前散发的氧气浓度。
                current_distribution.iat[i, j] = \
                    current_distribution.iat[i, j] + last_distribution.iat[i, j] - total_shared
            else:
                current_distribution.iat[i, j] = last_distribution.iat[i, j]

        print("process: " + f"{generation}/{MAX_ITERATION}")
        if generation % 1 == 0:
            fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
            show_oxygen_distribution(ax1, last_distribution, f"Generation: {generation - 1}")
            show_oxygen_distribution(ax2, current_distribution, f"Generation: {generation}")
            fig.tight_layout()
            fig.savefig(OUTPUT_DIR + str(generation))
            plt.close(fig)


if __name__ == "__main__":
    mkdirp(OUTPUT_DIR)
    init()
    iterate()

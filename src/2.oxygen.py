"""
氧气的扩散模型

规则：
1. 边界上的氧气浓度恒定为1，不扩散
"""


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from util import mkdirp


OUTPUT_DIR = "../out/2.oxygen/"

SIZE = 8
MAX_ITERATION = 16

initial_oxygen_distribution: pd.DataFrame
oxygen_distributions: [pd.DataFrame]


def init():
    global initial_oxygen_distribution, oxygen_distributions

    initial_oxygen_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=np.int8)
    for i in range(1, SIZE - 1):
        for j in range(1, SIZE - 1):
            initial_oxygen_distribution.iat[i, j] = np.random.rand()
    oxygen_distributions = [initial_oxygen_distribution.copy(), initial_oxygen_distribution.copy()]


def show_board(ax, board, title=None):
    global SIZE

    ax.imshow(board, cmap='Greys')
    ax.set_xticks(np.arange(0, SIZE, 1))
    ax.set_yticks(np.arange(0, SIZE, 1))
    ax.set_xticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_yticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_xticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.grid(which="minor", color='gray', linestyle='-', linewidth=2)
    if title:
        ax.title.set_text(title)


def iterate():
    for generation in range(1, MAX_ITERATION + 1):
        current_oxygen_distribution = oxygen_distributions[generation % 2]
        last_oxygen_distribution = oxygen_distributions[(generation + 1) % 2]

        for i in range(1, SIZE-1):
            for j in range(1, SIZE-1):
                total: int = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        total = total + last_oxygen_distribution.iat[i + x, j + y]
                total = total - last_oxygen_distribution.iat[i, j]
                if total >= 4 or total <= 1:
                    current_oxygen_distribution.iat[i, j] = 0
                elif total == 3:
                    current_oxygen_distribution.iat[i, j] = 1
                else:
                    current_oxygen_distribution.iat[i, j] = last_oxygen_distribution.iat[i, j]

        print("process: " + f"{generation}/{MAX_ITERATION}")
        if generation % 1 == 0:
            fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
            show_board(ax1, last_oxygen_distribution, f"Generation: {generation - 1}")
            show_board(ax2, current_oxygen_distribution, f"Generation: {generation}")
            fig.tight_layout()
            fig.savefig(OUTPUT_DIR + str(generation))
            plt.close(fig)


if __name__ == "__main__":
    mkdirp(OUTPUT_DIR)
    init()
    iterate()

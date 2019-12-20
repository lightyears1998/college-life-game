"""
生产者模型
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from util import mkdirp


OUTPUT_DIR = "../out/3.producer/"

SIZE = 8
CELLS = [(i, j) for i in range(0, SIZE) for j in range(0, SIZE)]

MAX_GENERATION = 32
CURRENT_GENERATION = 1

initial_oxygen_distribution: pd.DataFrame
oxygen_distributions: [pd.DataFrame]


def get_last_oxygen_distribution():
    return oxygen_distributions[(CURRENT_GENERATION + 1) % 2]


def get_current_oxygen_distribution():
    return oxygen_distributions[CURRENT_GENERATION % 2]


def init_oxygen():
    global initial_oxygen_distribution, oxygen_distributions

    initial_oxygen_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=float)
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            initial_oxygen_distribution.iat[i, j] = np.random.rand()
    oxygen_distributions = [initial_oxygen_distribution.copy(), initial_oxygen_distribution.copy()]


initial_producer_distribution: pd.DataFrame
producer_distributions: [pd.DataFrame]


def init_producer():
    global initial_producer_distribution, producer_distributions

    initial_producer_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=float)
    producer_distributions = [initial_producer_distribution.copy(), initial_producer_distribution.copy()]


sun_level = 1  # 光照强度


def init():
    init_oxygen()
    init_producer()


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


def oxygen_diffuse():
    global oxygen_distributions

    current_distribution = get_current_oxygen_distribution()
    last_distribution = get_last_oxygen_distribution()

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


def producer_produce_oxygen():
    pass


def producer_grow_density():
    pass


def producer_emerge():
    pass


def producer_action():
    pass


def plot_current_state():
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    show_oxygen_distribution(ax1, get_current_oxygen_distribution(), f"Generation: {CURRENT_GENERATION}")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR + str(CURRENT_GENERATION))
    plt.close(fig)


def iterate():
    global CURRENT_GENERATION

    plot_current_state()  # 打印初始状态
    while CURRENT_GENERATION < 32:
        CURRENT_GENERATION = CURRENT_GENERATION + 1

        oxygen_diffuse()
        producer_action()

        print("process: " + f"{CURRENT_GENERATION}/{MAX_GENERATION}")
        if CURRENT_GENERATION % 1 == 0:
            plot_current_state()


if __name__ == "__main__":
    mkdirp(OUTPUT_DIR)
    init()
    iterate()

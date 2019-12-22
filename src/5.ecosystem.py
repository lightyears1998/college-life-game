"""
模拟简单的生态系统
"""

import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from util import mkdirp


OUTPUT_DIR = "../out/4.consumer/"

SIZE = 8
CELLS = [(i, j) for i in range(0, SIZE) for j in range(0, SIZE)]

MAX_GENERATION = 128
CURRENT_GENERATION = 1
MICRO_TIME = 1

sun_level = 1  # 光照强度
initial_oxygen_distribution: pd.DataFrame
initial_producer_distribution: pd.DataFrame
initial_consumer_distribution: pd.DataFrame

oxygen_distributions: [pd.DataFrame]
producer_distributions: [pd.DataFrame]
consumer_distributions: [pd.DataFrame]


def get_last_oxygen_distribution():
    return oxygen_distributions[(MICRO_TIME + 1) % 2]


def get_current_oxygen_distribution():
    return oxygen_distributions[MICRO_TIME % 2]


def get_last_producer_distribution():
    return producer_distributions[(CURRENT_GENERATION + 1) % 2]


def get_current_producer_distribution():
    return producer_distributions[CURRENT_GENERATION % 2]


def get_last_consumer_distribution():
    return consumer_distributions[(CURRENT_GENERATION + 1) % 2]


def get_current_consumer_distribution():
    return consumer_distributions[CURRENT_GENERATION % 2]


def init_oxygen():
    global initial_oxygen_distribution, oxygen_distributions

    initial_oxygen_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=float)
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            initial_oxygen_distribution.iat[i, j] = np.random.rand() * 0.1
    oxygen_distributions = [initial_oxygen_distribution.copy(), initial_oxygen_distribution.copy()]


def init_producer():
    global initial_producer_distribution, producer_distributions

    initial_producer_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=float)
    initial_producer_distribution.iat[math.floor(SIZE/2), math.floor(SIZE/2)] = 0.2
    producer_distributions = [initial_producer_distribution.copy(), initial_producer_distribution.copy()]


def init_consumer():
    global initial_consumer_distribution, consumer_distributions

    initial_consumer_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=float)
    initial_consumer_distribution.iat[math.floor(SIZE / 2) + 1, math.floor(SIZE / 2) + 1] = 0.1
    consumer_distributions = [initial_consumer_distribution.copy(), initial_consumer_distribution.copy()]


def init():
    init_oxygen()
    init_producer()
    init_consumer()


def show_oxygen_distribution(ax):
    ax.imshow(get_current_oxygen_distribution(), interpolation='none', cmap="Blues", vmin=0, vmax=1)
    ax.title.set_text("Oxygen")
    ax.set_xticks(np.arange(0, SIZE, 1))
    ax.set_yticks(np.arange(0, SIZE, 1))
    ax.set_xticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_yticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_xticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.grid(which="minor", color='w', linestyle='-', linewidth=2)


def show_producer_distribution(ax):
    ax.imshow(get_current_producer_distribution(), interpolation='none', cmap="Greens", vmin=0.01, vmax=1)
    ax.title.set_text("Producer")
    ax.set_xticks(np.arange(0, SIZE, 1))
    ax.set_yticks(np.arange(0, SIZE, 1))
    ax.set_xticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_yticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_xticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.grid(which="minor", color='w', linestyle='-', linewidth=2)


def show_consumer_distribution(ax):
    ax.imshow(get_current_consumer_distribution(), interpolation='none', cmap="Reds", vmin=0.01, vmax=1)
    ax.title.set_text("Consumer")
    ax.set_xticks(np.arange(0, SIZE, 1))
    ax.set_yticks(np.arange(0, SIZE, 1))
    ax.set_xticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_yticklabels(np.arange(1, SIZE + 1, 1))
    ax.set_xticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-.5, SIZE, 1), minor=True)
    ax.grid(which="minor", color='w', linestyle='-', linewidth=2)


def oxygen_diffuse():
    global MICRO_TIME

    MICRO_TIME = MICRO_TIME + 1
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
            diffusion_oxygen = last_distribution.iat[i, j] / 2  # 散发当前格子氧气浓度的一半
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


def density_curve(input_density):
    if input_density > 1:
        return 1
    elif input_density < 0.01:
        return 0
    else:
        return 1 - (input_density-1)**2


def producer_produce_oxygen():
    # 本轮氧气交换已经计算完毕，而生产者种群密度还未计算完毕。
    oxygen_distribution = get_current_oxygen_distribution()
    producer_distribution = get_last_producer_distribution()

    for i, j in CELLS:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                ti, tj = (i + dx + SIZE) % SIZE, (j + dy + SIZE) % SIZE
                producer_density = producer_distribution.iat[ti, tj]
                if producer_density > 0:
                    oxygen_level = oxygen_distribution.iat[ti, tj]
                    produce_oxygen = sun_level * producer_density * max(1 - oxygen_level, 0)
                    oxygen_distribution.iat[ti, tj] = oxygen_level + produce_oxygen


def producer_grow_density():
    last_distribution = get_last_producer_distribution()
    current_distribution = get_current_producer_distribution()

    for i, j in CELLS:
        density = last_distribution.iat[i, j]
        growth = (density_curve(density) - density) * sun_level
        current_distribution.iat[i, j] = density + growth


def producer_emerge():
    distribution = get_current_producer_distribution()

    for i, j in CELLS:
        density = distribution.iat[i, j]
        if density > 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    ti, tj = (i + dx + SIZE) % SIZE, (j + dy + SIZE) % SIZE
                    if distribution.iat[ti, tj] < 0.01 and np.random.rand() < density / 8:
                        distribution.iat[ti, tj] = 0.02


def producer_action():
    producer_produce_oxygen()
    producer_grow_density()
    producer_emerge()


def consumer_grow_density():
    # 只有满足了氧气和食物的需求才能增长。
    consumer_distribution = get_last_consumer_distribution()
    oxygen_distribution = get_current_oxygen_distribution()
    producer_distribution = get_current_producer_distribution()

    for i, j in CELLS:
        density = consumer_distribution.iat[i, j]
        if density > 0.01:
            oxygen_satisfied, food_satisfied = True, True

            need_oxygen = 0.5 * density
            actual_oxygen = oxygen_distribution.iat[i, j]
            if actual_oxygen < need_oxygen:
                density = density * (actual_oxygen / need_oxygen)
                need_oxygen = actual_oxygen
                oxygen_satisfied = False

            need_food = 0.5 * density
            actual_producer = producer_distribution.iat[i, j]
            if actual_producer < need_food:
                density = density * (0.5 + 0.5*(actual_producer / need_food))
                need_food = actual_producer
                food_satisfied = False

            if oxygen_satisfied and food_satisfied:
                density = density_curve(density)

            consumer_distribution.iat[i, j] = density
            oxygen_distribution.iat[i, j] = actual_oxygen - need_oxygen
            producer_distribution.iat[i, j] = actual_producer - need_food
        else:
            consumer_distribution.iat[i, j] = 0


def consumer_move():
    # 由周边格子的氧气和食物分布决定移动方向。
    last_distribution = get_last_consumer_distribution()
    current_distribution = get_current_consumer_distribution()
    oxygen_distribution = get_current_oxygen_distribution()
    producer_distribution = get_current_producer_distribution()

    for i, j in CELLS:
        current_distribution.iat[i, j] = last_distribution.iat[i, j]

    for i, j in CELLS:
        density = last_distribution.iat[i, j]
        if density > 0:
            candidates = []
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    ti, tj = (i + dx + SIZE) % SIZE, (j + dy + SIZE) % SIZE
                    if last_distribution.iat[ti, tj] == 0 and current_distribution.iat[ti, tj] == 0:
                        oxygen = oxygen_distribution.iat[ti, tj]
                        producer = producer_distribution.iat[ti, tj]
                        score = oxygen * 0.6 + producer * 0.4
                        candidates.append((score, (ti, tj)))
            if len(candidates) > 0:
                candidates.sort(key=lambda tup: tup[0], reverse=True)
                _, (ti, tj) = candidates[0]
                current_distribution.iat[ti, tj] = density
                current_distribution.iat[i, j] = 0
            else:
                current_distribution.iat[i, j] = density


def consumer_emerge():
    distribution = get_current_consumer_distribution()

    for i, j in CELLS:
        density = distribution.iat[i, j]
        if density > 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    ti, tj = (i + dx + SIZE) % SIZE, (j + dy + SIZE) % SIZE
                    if distribution.iat[ti, tj] < 0.01 and np.random.rand() < density / 8:
                        distribution.iat[ti, tj] = 0.02


def consumer_action():
    consumer_grow_density()
    consumer_move()
    consumer_emerge()


def plot_current_state():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
    show_oxygen_distribution(ax1)
    show_producer_distribution(ax2)
    show_consumer_distribution(ax3)
    fig.suptitle(f"Generation {CURRENT_GENERATION}")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR + str(CURRENT_GENERATION))
    plt.close(fig)


def iterate():
    global CURRENT_GENERATION

    plot_current_state()  # 打印初始状态
    while CURRENT_GENERATION < MAX_GENERATION:
        CURRENT_GENERATION = CURRENT_GENERATION + 1

        for _ in range(4):
            oxygen_diffuse()
        producer_action()
        consumer_action()

        print("process: " + f"{CURRENT_GENERATION}/{MAX_GENERATION}")
        print(get_current_consumer_distribution())

        if CURRENT_GENERATION % 1 == 0:
            plot_current_state()


if __name__ == "__main__":
    mkdirp(OUTPUT_DIR)
    init()
    iterate()

"""
尝试用多线程的方法优化运算效率，
但是这方面的探索暂时失败了。
因为线程间共享变量不是扔一个全局变量就可以解决的。
还是日后时间富裕了再进行这方面的研究吧。
"""


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multiprocessing import Pool


SIZE = 64
MAX_GENERATION = 16000
CURRENT_GENERATION = 0


initial_oxygen_distribution = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=np.int8)
oxygen_distributions = [initial_oxygen_distribution, initial_oxygen_distribution]
active_position = [(x, y) for x in range(1, SIZE - 1) for y in range(1, SIZE - 1)]


def init():
    global oxygen_distributions

    for i in range(1, SIZE - 1):
        for j in range(1, SIZE - 1):
            initial_oxygen_distribution.iat[i, j] = np.random.randint(2)
    boards = [initial_oxygen_distribution, initial_oxygen_distribution]


def calculate(location: (int, int)):
    global oxygen_distributions

    x, y = location
    current_board = boards[CURRENT_GENERATION % 2]
    last_board = boards[(CURRENT_GENERATION + 1) % 2]

    total = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            total = total + last_board.iat[x + dx, y + dy]
    total = total - last_board.iat[x, y]
    if total >= 4 or total <= 1:
        current_board.iat[x, y] = 0
    if total == 3:
        current_board.iat[x, y] = 1


def main():
    global CURRENT_GENERATION, MAX_GENERATION

    init()
    while CURRENT_GENERATION <= MAX_GENERATION:
        pool = Pool()
        pool.map(calculate, active_position)

        print("process: " + f"{CURRENT_GENERATION}/{MAX_GENERATION}")
        if CURRENT_GENERATION % 100 == 0:
            plt.matshow(oxygen_distributions[CURRENT_GENERATION % 2])
            plt.title("Generation " + str(CURRENT_GENERATION))
            plt.savefig(str(CURRENT_GENERATION))
        CURRENT_GENERATION = CURRENT_GENERATION + 1


if __name__ == '__main__':
    main()

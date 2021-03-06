"""
基本的元胞自动机（康威生命游戏）

规则：
0. 边界上的细胞状态永远不变，永远为死亡状态。
1. 中心格子周边8个格子内细胞数量等于3则出生。
2. 中心格子周边8个各自内细胞数量大于等于4或小于等于1则死亡。
3. 其他情况下中心格子状态保持不变。

程序先随机地给定棋盘内细胞初始状态，并按照康威生命游戏规则演化指定代数。
"""


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from util import mkdirp


OUTPUT_DIR = "../out/1.basic/"

SIZE = 8
MAX_ITERATION = 16

initial_board: pd.DataFrame
boards: [pd.DataFrame]


def init():
    global initial_board, boards

    initial_board = pd.DataFrame(data=np.zeros([SIZE, SIZE]), dtype=np.int8)
    for i in range(1, SIZE - 1):
        for j in range(1, SIZE - 1):
            initial_board.iat[i, j] = np.random.randint(2)
    boards = [initial_board.copy(), initial_board.copy()]


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
    global boards

    for generation in range(1, MAX_ITERATION + 1):
        current_board = boards[generation % 2]
        last_board = boards[(generation + 1) % 2]

        for i in range(1, SIZE-1):
            for j in range(1, SIZE-1):
                total: int = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        total = total + last_board.iat[i + x, j + y]
                total = total - last_board.iat[i, j]
                if total >= 4 or total <= 1:
                    current_board.iat[i, j] = 0
                elif total == 3:
                    current_board.iat[i, j] = 1
                else:
                    current_board.iat[i, j] = last_board.iat[i, j]

        print("process: " + f"{generation}/{MAX_ITERATION}")
        if generation % 1 == 0:
            fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
            show_board(ax1, last_board, f"Generation: {generation - 1}")
            show_board(ax2, current_board, f"Generation: {generation}")
            fig.tight_layout()
            fig.savefig(OUTPUT_DIR + str(generation))
            plt.close(fig)


if __name__ == "__main__":
    mkdirp(OUTPUT_DIR)
    init()
    iterate()

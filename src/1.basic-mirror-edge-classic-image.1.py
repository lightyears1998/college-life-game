"""
生命游戏的经典图像

规则：
0. 镜像边界
1. 周边8个格子内细胞数量等于3则出生。
2. 周边8个格子内细胞数量大约等于4或小于等于1则死亡。
3. 其他情况下格子状态保持不变。
"""


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from util import mkdirp


OUTPUT_DIR = "../out/1.basic.经典稳定图像/"

SIZE = 11
CELLS = [(i, j) for i in range(0, SIZE) for j in range(0, SIZE)]

MAX_ITERATION = 4

initial_board: pd.DataFrame
boards: [pd.DataFrame]


def init():
    global initial_board, boards

    data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    initial_board = pd.DataFrame(data=data, dtype=np.int8)
    boards = [initial_board.copy(), initial_board.copy()]


def show_board(ax, board, title=None):
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

        for i, j in CELLS:
            total = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    total = total + last_board.iat[(i + x + SIZE) % SIZE, (j + y + SIZE) % SIZE]
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

import time
import tracemalloc
from algorithm import astar
from astar import read_board
from BoardCreation import create_board


def run_with_size(size, heuristic):
    print("on size " + str(size))
    filename = create_board(size, size)
    board, start, end = read_board(filename)
    stime = time.time()
    tracemalloc.start()
    astar(board, start, end, heuristic, False)
    bytes_used = tracemalloc.get_traced_memory()[1]
    print("Bytes used: " + str(bytes_used))
    tracemalloc.stop()
    etime = time.time()
    dif = etime - stime
    print("took " + str(round(dif, 2)) + " seconds")
    return dif


def test_size_for_time_on_heuristic(goal_time, heuristic):
    size = 10
    while True:
        print("on size " + str(size))
        filename = create_board(size, size)
        board, start, end = read_board(filename)
        stime = time.time()
        astar(board, start, end, heuristic)
        etime = time.time()
        dif = etime - stime
        print("took " + str(round(dif, 2)) + " seconds")
        if dif > goal_time:
            return size
        size *= 2


def average(li):
    s = sum(li)
    return s / len(li)


if __name__ == '__main__':
    # somewhere between 640 and 1280
    # 690 seems to work well (nice)
    # run_with_size(1000, 4)

    run_with_size(100, 0)
    run_with_size(300, 4)

    #size = 690

    #filenames = []
    #for i in range(10):
    #    filenames.append(create_board(size, size))

    #heuristics = [1, 2, 3, 4, 5, 6]

    #for file in filenames:
    #    board, start, end = read_board(file)
    pass

import time
import argparse
from algorithm import *
from BoardCreation import *


def read_board(filename):
    f = open(filename, 'r')

    board = []
    row = 0
    col = 0

    start = -1
    end = -1

    # Loop through the file line by line and add to the 2D array
    for line in f.readlines():
        row_set = []
        for char in line:
            if char.isdigit():
                row_set.append(int(char))
                col += 1
            else:
                if char == 'G':
                    row_set.append(1)
                    end = (row, col)
                    col += 1
                elif char == 'S':
                    row_set.append(1)
                    start = (row, col)
                    col += 1
        board.append(row_set)
        row += 1
        col = 0

    f.close()

    return board, start, end


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # test_all()
    # print("Tests Passed!")
    # create_board(800, 800)

    parser = argparse.ArgumentParser()

    '''
        Example of running the file with the command line argument:

        > python3 ./astar.py Sample\ Board.txt
    '''
    parser.add_argument(
        'file',
        help="--file : the name of the file you want to be read in",
        type=str
    )
    parser.add_argument(
        'heuristic',
        help="--heuristic : the name of the file you want to be read in",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7]
    )

    args = parser.parse_args()

    print(args.file)
    print(args.heuristic)

    #board, start, end = read_board(args.file)

    total_time = 1 #If we want to do a time goal add it here in seconds
    start_time = time.time()
    while total_time > (time.time() - start_time):
        board, start, end = create_board_array(10, 10)
        astar(board, start, end, args.heuristic)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

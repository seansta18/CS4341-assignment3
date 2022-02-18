import random
import time

list = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def create_board_array(x, y):
    board = []

    for r in range(x):
        temp = []
        for c in range(y):
            temp.append(random.choice(list))
        board.append(temp)

    start = (random.choice(list), random.choice(list))
    board[start[0]][start[1]] = 1
    end = (random.choice(list), random.choice(list))
    board[end[0]][end[1]] = 1

    return board, start, end

def create_board(row, col, counter):
    start_tuple = (random.choice(range(row)), random.choice(range(col)))
    end_tuple = (random.choice(range(row)), random.choice(range(col)))
    if start_tuple == end_tuple:
        create_board(row, col, counter)
        return
    filename = time.strftime("%H%M%S")
    filename = filename + str(counter)
    with open(filename, 'w') as file:
        for i in range(row):
            for j in range(col):
                if start_tuple[0] == i and start_tuple[1] == j:
                    file.write("S")
                elif end_tuple[0] == i and end_tuple[1] == j:
                    file.write("G")
                else:
                    file.write(str(random.choice(list)))
                file.write("\t")
            file.write("\n")
    return filename

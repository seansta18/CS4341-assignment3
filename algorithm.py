from pqdict import pqdict
import math
import csv

# constants for tuples

# for indexing moves
POS = 0
DIR = 1

# for indexing positions
X = 0
Y = 1

# Possible values for direction
# Assigned like that so modulo 4 incrementing/decrementing will turn right and left
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# For indexing action_datum
MOVE = 0
ACTION = 1

# Possible values for actions
FORWARD = 0
LEFT = 1
RIGHT = 2
BASH = 3

test_board = [[4, 1, 4, 6],
              [2, 9, 9, 6],
              [1, 4, 1, 3]]


def num_to_dir(n):
    if n == NORTH:
        return "NORTH"
    if n == SOUTH:
        return "SOUTH"
    if n == WEST:
        return "WEST"
    if n == EAST:
        return "EAST"

    return "None"


def num_to_action(n):
    if n == FORWARD:
        return "FORWARD"
    if n == LEFT:
        return "LEFT"
    if n == RIGHT:
        return "RIGHT"
    if n == BASH:
        return "BASH"

    return "None"


# heuristic function
def get_heuristic(curr_pd, end, choice, board):
    current_pos = curr_pd[POS]
    horiz_dist = abs(current_pos[X] - end[X])
    vert_dist = abs(current_pos[Y] - end[Y])

    if choice == 1:
        return 0
    elif choice == 2:
        return min(horiz_dist, vert_dist)
    elif choice == 3:
        return max(horiz_dist, vert_dist)
    elif choice == 4:
        return horiz_dist + vert_dist
    elif choice == 5:
        manhattan_dist = horiz_dist + vert_dist
        return admissible_heuristic(curr_pd, board, manhattan_dist)
    else:
        manhattan_dist = horiz_dist + vert_dist
        return 3 * admissible_heuristic(curr_pd, board, manhattan_dist)


def admissible_heuristic(curr_pd, board, manhattan_dist):
    actions = next_actions(curr_pd, len(board), len(board[0]))
    # print('\nCurr_pd: (', curr_pd[0][X], ',', curr_pd[0][Y], ')')

    # print('\t', actions)

    min_cost = 9

    for action in actions:  # action is a ((POS, DIR), ACTION)
        new_g = timecost(action, board)
        # print('\t\t :', new_g)

        if min_cost > new_g:
            min_cost = new_g

    # print('\t\t Min Cost:', minCost)
    new_heuristic = manhattan_dist - 1 + min_cost

    return new_heuristic


STEP_OOB = -1


# returns the position of taking n steps in the direction you're currently
# facing from your current position
# returns -1 if steps off the board
def step(curr_pd, n, bx, by):
    direction = curr_pd[DIR]
    position = curr_pd[POS]
    # print(str(curr_pd))
    x = position[X]
    y = position[Y]

    # print(str(x))
    # print(str(y))

    if direction == NORTH:
        x -= n
    if direction == SOUTH:
        x += n
    if direction == EAST:
        y += n
    if direction == WEST:
        y -= n

    if x < 0 or y < 0 or x >= bx or y >= by:
        return -1

    return (x, y), direction


# returns True if we can make action from curr_pd on the board
def valid_action(curr_pd, action, bx, by):
    if action == BASH:
        if step(curr_pd, 2, bx, by) == STEP_OOB:
            return False

    if action == FORWARD:
        if step(curr_pd, 1, bx, by) == STEP_OOB:
            return False

    if action == LEFT:
        if step((curr_pd[POS], (curr_pd[DIR] - 1) % 4), 1, bx, by) == STEP_OOB:
            return False

    if action == RIGHT:
        if step((curr_pd[POS], (curr_pd[DIR] + 1) % 4), 1, bx, by) == STEP_OOB:
            return False

    return True


def next_actions(curr_pd, bx, by):
    actions = []
    for action in range(4):
        if valid_action(curr_pd, action, bx, by):
            if action == LEFT:
                actions.append(((curr_pd[POS], (curr_pd[DIR] - 1) % 4), LEFT))
            elif action == RIGHT:
                actions.append(((curr_pd[POS], (curr_pd[DIR] + 1) % 4), RIGHT))
            elif action == FORWARD:
                new_pd = step(curr_pd, 1, bx, by)
                actions.append((new_pd, FORWARD))
            elif action == BASH:
                new_pd = step(curr_pd, 2, bx, by)
                actions.append((new_pd, BASH))
    return actions


# action_datum contains a (MOVE, ACTION) where MOVE is a (POS, DIR) where the move ends, and ACTION
# is the action taken to get there
def timecost(action_datum, board):
    if action_datum[ACTION] == 0:  # Forward
        return board[action_datum[MOVE][POS][X]][action_datum[MOVE][POS][Y]]
    elif action_datum[ACTION] == 1:  # Left
        return math.ceil(board[action_datum[MOVE][POS][X]][action_datum[MOVE][POS][Y]] / 2)
    elif action_datum[ACTION] == 2:  # Right
        return math.ceil(board[action_datum[MOVE][POS][X]][action_datum[MOVE][POS][Y]] / 2)
    elif action_datum[ACTION] == 3:  # Bash
        return 3 + board[action_datum[MOVE][POS][X]][action_datum[MOVE][POS][Y]]

# returns the value of the squares immediately adjacent to the robot
def neighborValue(xloc, yloc, board):
    return [board[xloc - 1][yloc - 1], board[xloc - 1][yloc], board[xloc - 1][yloc + 1],
            board[xloc][yloc - 1], board[xloc][yloc + 1],
            board[xloc + 1][yloc - 1], board[xloc + 1][yloc], board[xloc + 1][yloc + 1]]

list_of_nValues = []

# board is a 2d array, start is (X, Y), end is (X, Y)
def astar(board, start, end, heuristic, print_results=True):
    start_pd = (start, NORTH)

    # This pred dict takes in a move_pd as a key and returns ((POS, DIR), ACTION) where (POS, DIR)
    # is where you came from to get to move_pd and ACTION is the action taken to get to move_pd
    pred = {start_pd: 0}  # end the backwards reconstruction of the path at pred[curr] == 0

    g = {start_pd: 0}  # tracks the smallest g score for each pos-dir
    h = {start_pd: get_heuristic(start_pd, end, heuristic, board)}
    f = {start_pd: g[start_pd] + h[start_pd]}  # tracks that smallest f score for each pd

    minpq = pqdict()
    minpq.additem(start_pd, f[start_pd])

    nodes_expanded = 0
    real_end = -1
    while len(minpq.keys()) > 0:
        curr = minpq.popitem()[0]

        if curr[POS] == end:
            real_end = curr  # embeds the direction we ended on to start backtracking
            break

        for action_datum in next_actions(curr, len(board), len(board[0])):  # action_datum is a ((POS, DIR), ACTION)
            move_pd = action_datum[MOVE]
            new_g = g[curr] + timecost(action_datum, board)

            visited = move_pd in g.keys()
            if visited and new_g >= g[move_pd]:
                continue  # we're at an old location in a slower way, SKIP

            g[move_pd] = new_g
            h[move_pd] = get_heuristic(move_pd, end, heuristic, board)
            f[move_pd] = g[move_pd] + h[move_pd]

            nodes_expanded += 1
            minpq[move_pd] = f[move_pd]

            # leave breadcrumbs
            pred[move_pd] = (curr, action_datum[ACTION])

    path = []
    curr = (real_end, None)
    #  Backtracking
    while curr != 0:
        path.append(curr)
        curr = pred[curr[MOVE]]

    path.reverse()

    # process path to 'fix' bash macro
    processed_path = []
    for action in path:
        move_pd = action[MOVE]
        processed_path.append(action)
        if action[ACTION] == BASH:
            processed_path.append((step(move_pd, 1, len(board), len(board[0])), FORWARD))

    states = []
            
    if print_results:
        print("Start path...")
        for action in processed_path:
            if action == processed_path[len(processed_path) - 1]:
                print("End at " + str(action[MOVE][POS]) + " " + num_to_dir(action[MOVE][DIR]) + "...")
            else:
                print("From " + str(action[MOVE][POS]) + " " + num_to_dir(action[MOVE][DIR]) + " make action " +
                      num_to_action(action[ACTION]))
                
                states.append(num_to_action(action[ACTION]))

        
        total_cost = f[real_end]
        print("Total time cost was " + str(total_cost))
        print("Number of actions: " + str(len(processed_path) - 1))
        print("Score is " + str(100 - total_cost))
        print("Expanded " + str(nodes_expanded) + " nodes")

    # write to csv
    # currently only have one col: state
    with open('data.csv', 'w', newline='') as csvfile:
        fieldnames = ['State', 'Neighbor Values', None]
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames);
        thewriter.writeheader()
        for state in states:
            thewriter.writerow({'State': state}) 
    
    total_cost = f[real_end]
    return processed_path, total_cost, nodes_expanded

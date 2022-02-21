from pqdict import pqdict
import math
import pandas as pd

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
    elif choice == 6:
        manhattan_dist = horiz_dist + vert_dist
        return 3 * admissible_heuristic(curr_pd, board, manhattan_dist)
    else:
        return 5.3919 * horiz_dist + 5.4093 * vert_dist - 65.7739


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

def inBounds(x, y, board):
    if x < 0:
        return False
    if y < 0:
        return False
    if x >= len(board):
        return False
    if y >= len(board):
        return False

    return True


# returns the value of the squares immediately adjacent to the robot
def neighborValue(xloc, yloc, board):
    values = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                pass
            elif inBounds(x + xloc, y + yloc, board):
                values.append(board[xloc + x][yloc + y])
            else:
                values.append(999999)

    return values


list_of_nValues = []


# returns a list of x distances from goal
def xDistFromGoal(goal_x, list_of_x):
    x_dist = []

    for x in list_of_x:
        diff = abs(goal_x - x)
        x_dist.append(diff)
    return x_dist


# returns a list of y distances from goal
def yDistFromGoal(goal_y, list_of_y):
    y_dist = []

    for y in list_of_y:
        diff = abs(goal_y - y)
        y_dist.append(diff)
    return y_dist


#For output to csv
states = []
x_poses = []
y_poses = []
costs = []
surrounding_1 = []
surrounding_2 = []
surrounding_3 = []
surrounding_4 = []
surrounding_5 = []
surrounding_6 = []
surrounding_7 = []
surrounding_8 = []



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

    goal_x = processed_path[len(processed_path) - 1][0][0][0]
    goal_y = processed_path[len(processed_path) - 1][0][0][1]


    if print_results:
        print("\n\nStart path...")
        lastMoveCost = 0
        for action in processed_path:
            if action == processed_path[len(processed_path) - 1]:
                print("End at " + str(action[MOVE][POS]) + " " + num_to_dir(action[MOVE][DIR]) + "...")
                states.append("Goal")
                x_poses.append(abs(goal_x - action[MOVE][POS][0]))
                y_poses.append(abs(goal_y - action[MOVE][POS][1]))
                values = neighborValue(action[MOVE][POS][0], action[MOVE][POS][1], board)
                surrounding_1.append(values[0])
                surrounding_2.append(values[1])
                surrounding_3.append(values[2])
                surrounding_4.append(values[3])
                surrounding_5.append(values[4])
                surrounding_6.append(values[5])
                surrounding_7.append(values[6])
                surrounding_8.append(values[7])
                costs.append(1)
            if action == processed_path[0]:
                print("Start at " + str(action[MOVE][POS]) + " " + num_to_dir(action[MOVE][DIR]) + "...")
                states.append("Start")
                x_poses.append(abs(goal_x - action[MOVE][POS][0]))
                y_poses.append(abs(goal_y - action[MOVE][POS][1]))
                values = neighborValue(action[MOVE][POS][0], action[MOVE][POS][1], board)
                surrounding_1.append(values[0])
                surrounding_2.append(values[1])
                surrounding_3.append(values[2])
                surrounding_4.append(values[3])
                surrounding_5.append(values[4])
                surrounding_6.append(values[5])
                surrounding_7.append(values[6])
                surrounding_8.append(values[7])
                costs.append(f[real_end])
                lastMoveCost = f[real_end]
            if action == processed_path[len(processed_path) - 1]:
                pass #avoid writing "None" action state to file
            else:
                print("From " + str(action[MOVE][POS]) + " " + num_to_dir(action[MOVE][DIR]) + " make action " +
                      num_to_action(action[ACTION]))

                x_poses.append(abs(goal_x - action[MOVE][POS][0]))
                y_poses.append(abs(goal_y - action[MOVE][POS][1]))
                values = neighborValue(action[MOVE][POS][0], action[MOVE][POS][1], board)
                surrounding_1.append(values[0])
                surrounding_2.append(values[1])
                surrounding_3.append(values[2])
                surrounding_4.append(values[3])
                surrounding_5.append(values[4])
                surrounding_6.append(values[5])
                surrounding_7.append(values[6])
                surrounding_8.append(values[7])
                states.append(num_to_action(action[ACTION]))
                costs.append(lastMoveCost - f[action[MOVE]]) #TODO: cost of this node = last node cost - this node cost; please check that this works as it should
                lastMoveCost = lastMoveCost - f[action[MOVE]]

        total_cost = f[real_end]
        print("Total time cost was " + str(total_cost))
        print("Number of actions: " + str(len(processed_path) - 1))
        print("Score is " + str(100 - total_cost))
        print("Expanded " + str(nodes_expanded) + " nodes")

    dict = {'top left': surrounding_1,'top': surrounding_2, 'top right': surrounding_3, 'left': surrounding_4, 'right': surrounding_5, 'bottom left': surrounding_6, 'bottom': surrounding_7, 'bottom right': surrounding_8, 'x distance': x_poses, 'y distance': y_poses, 'A* cost to goal (dependant)' : costs}
    df = pd.DataFrame(dict)
    df.to_csv('data.csv')

    total_cost = f[real_end]
    return processed_path, total_cost, nodes_expanded

# def getState():
#   return states;

# def getXDists():
#    return xDistFromGoal(goal_x, x_poses)

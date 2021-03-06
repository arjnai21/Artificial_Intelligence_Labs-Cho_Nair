# Lab 1, Part 2: Informed Search.
# Name(s): Arjun Nair, Elias Cho


#command to test: python lab1_part2_gui.py slidepuzzle test_puzzles/test_puzzle01.txt

import random
from priorityqueue import PriorityQueue
from statenode import StateNode

from roomba_multi_state import FLOOR, CARPET, WALL, GOAL

INF = float('inf')

"""
Provided for you: two starter heuristics that you don't have to edit.
"""

"""
A very unhelpful heuristic. Returns 0. But it's admissible and consistent!
"""
def zero_heuristic(state):
    return 0

"""
A heuristic for RoombaRouteState: assuming there is only
one dirty tile (one goal state), return the manhattan distance to that dirty tile.
Both admissible and consistent!
"""
def roomba_manhattan_onegoal(roomba_state):
    grid = roomba_state.get_grid()
    pos_r, pos_c = roomba_state.get_position()

    for r in range(roomba_state.get_height()):
        for c in range(roomba_state.get_width()):
            if grid[r][c] == GOAL : # Find the goal position
                # Return manhattan distance between roomba and goal
                return abs(r - pos_r) + abs(c - pos_c)
    return 0


#### Lab 1, Part 2a: Informed Search #################################################

def GreedyBest(initial_state, heuristic_fn, # heuristic function must be provided
        avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for
    frontier = PriorityQueue()
    frontier.append(initial_state, heuristic_fn(initial_state))

    extended_filter = set()

    while frontier:  # frontier is False when it is empty. So just keep going until out of places to go...

        # choose next state to "extend" from frontier
        ext_node = frontier.pop()

        if (filtering and ext_node.get_all_features() in extended_filter):
            continue

        extended_filter.add(ext_node.get_all_features())

        counter['num_extends'] += 1

        # are we there? If so, return the node.
        if ext_node.is_goal_state():
            return ext_node

        # Update our caller (e.g. GUI) with the state we're extending.
        # Terminate search early if True is returned.
        if (state_callback_fn(ext_node)):
            break

        ### Update frontier with next states
        for state in ext_node.generate_next_states():
            if (avoid_backtrack and ext_node.get_parent() == state):
                continue

            if (filtering and state.get_all_features() in extended_filter):
                continue

            if (cutoff != INF and state.get_path_length() > cutoff):
                continue

            frontier.append(state, heuristic_fn(state))
            counter['num_enqueues'] += 1

    # if loop breaks before finding goal, search is failure; return None
    return None


def AStar(initial_state, heuristic_fn, # heuristic function must be provided
        avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for

    frontier = PriorityQueue()
    frontier.append(initial_state, initial_state.get_path_cost() + heuristic_fn(initial_state))

    extended_filter = set()

    while frontier:  # frontier is False when it is empty. So just keep going until out of places to go...

        # choose next state to "extend" from frontier
        ext_node = frontier.pop()

        if (filtering and ext_node.get_all_features() in extended_filter):
            continue

        extended_filter.add(ext_node.get_all_features())

        counter['num_extends'] += 1

        # are we there? If so, return the node.
        if ext_node.is_goal_state():
            return ext_node

        # Update our caller (e.g. GUI) with the state we're extending.
        # Terminate search early if True is returned.
        if (state_callback_fn(ext_node)):
            break

        ### Update frontier with next states
        for state in ext_node.generate_next_states():
            if (avoid_backtrack and ext_node.get_parent() == state):
                continue

            if (filtering and state.get_all_features() in extended_filter):
                continue

            if (cutoff != INF and state.get_path_length() > cutoff):
                continue

            frontier.append(state, state.get_path_cost() + heuristic_fn(state))
            counter['num_enqueues'] += 1

    # if loop breaks before finding goal, search is failure; return None
    return None


#### Lab 1, Part 2b: Slide Puzzle Heuristics #################################################

"""
First, implement these two heuristic functions for SlidePuzzleStates. Test them
using them with GreedyBestSearch and AStarSearch in the GUI.

Both heuristics, correctly implemented, will guarantee A* Search to find optimal solutions,
since they are both admissible and consistent, and much much faster than UCS.
Manhattan is generally much better than Hamming (why?), and A* can handle many of the
test puzzles in no more than a few seconds if you turn off the visualizer.
However, some of the most difficult puzzles might still take a while...
"""

"""
Return the Hamming distance (number of tiles out of place) of the SlidePuzzleState
"""
def slidepuzzle_hamming(puzzle_state):
    count = 0
    incorrect = 0
    grid = puzzle_state.grid
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != count and grid[i][j] != 0:
                incorrect += 1
            count +=1
    return incorrect

"""
Return the sum of Manhattan distances between tiles and goal of the SlidePuzzleState
"""

#goal location: [][num % gridSize]
def slidepuzzle_manhattan(puzzle_state):
    distance = 0
    grid = puzzle_state.grid
    for i in range(len(grid)):
        for j in range(len(grid)):
            distance += abs(i - grid[i][j] // len(grid)) + abs(j-grid[i][j] % len(grid)) #get goal coordinates and subtract from current
    return distance



#### Lab 1, Part 2c: Roomba Route MULTI-DIRT Heuristics #################################################

"""
You must write 2 NONTRIVIAL heuristics for RoombaMultiRouteState.
(Nontrivial means not simply zero, and also not calculating the exact remaining distance).

The first heuristic should help Greedy Best Search and A* Search onverge more quickly,
but it need not guarantee an optimal solution path.

The second heuristic should make A* Search converge quickly on an optimal path.
To guarantee optimality w/out extended filtering ,  your heuristic must be *admissible*.
Admissible means the heuristic never overestimates the distance to the goal.
To guarantee optimality w/ extended filtering, your heuristic must also be  *consistent*.
Consistent implies admissibility, but has the additional condition: if an action transition
costs c, taking that action never causes the heuristic to decrease more than c.
You will get full credit for this part ONLY if your heuristic is BOTH
admissible and consistent, but if you can only manage admissibility that will still
yield most of the points.

In both cases, *quickly* means two things:
1) the heuristic itself should be quick to calculate - doing as much work as another full search
defeates the purpose of using a heuristic!
2) the heuristic should help informed algorithms look at significantly fewer states than
UCS, especially in bigger mazes. You may see a more pronounced effect if the extended filter is turned OFF.

You may certainly create more than these two heuristics; if you do, add them to the
all_multi_heuristics dict for the GUI to see.

A mini-contest of heuristics will be held - if you have a particularly helpful and/or creative
heuristic, you might win! Win what, you ask? At the very least, artificial glory and honor...
"""

def roomba_multi_heuristic_basic(roomba_state):
    current = roomba_state.get_position()
    distances = [(((current[0] - i[0])**2 + (current[1] - i[1])**2)**.5) for i in roomba_state.get_dirt_locations()] #euclidean distance
    if distances:
        return sum(distances)
    else:
        return 0

def roomba_multi_heuristic_advanced(roomba_state):
    current = roomba_state.get_position()
    distances = [(abs(current[0] - i[0]) + abs(current[1] - i[1])) for i in roomba_state.get_dirt_locations()]
    if distances:
        return min(distances)
    else:
        return 0

all_multi_heuristics = {"Basic Heur.": roomba_multi_heuristic_basic,
                        "Adv. Heur.": roomba_multi_heuristic_advanced}

"""
Lastly, you must create one or more of your own multiple-dirt mazes to illustrate your
heuristics' effectiveness. It should be challenging enough so that your heuristics
make significant improvement over uninformed algorithms.

Your mazes should be in files named maze_multi_[ID]_[##].txt
ID should be your 6-char bergen ID (usually 3 letters of first name, 3 letters of last name)
## should be 01, then 02, etc.
The format of the files are as follows:
First row: 2 ints specifying the number of rows and cols in the maze
Second row: 2 ints specifying the initial row and col of the roomba
Remaining rows: Terrain of the maze. Be sure to not have extra spaces at the ends of lines.
'.' : Floor (cost 1 to move onto)
'~' : carpet (cost 2 to move onto)
'#' : Wall (can't move onto)
'G' : Dirt (costs 1 to move onto, and 1 to clean)
"""

# Lab 1, Part 1: Uninformed Search.
# Name(s): Arjun Nair, Elias Cho

import random
from collections import deque
from priorityqueue import PriorityQueue
from statenode import StateNode

INF = float('inf')

#### Lab 1, Part 1a: Uninformed Search #################################################


# command to run: python lab1_part1_gui.py roomba test_mazes/maze_02.txt

"""
### HELPFUL NOTES ABOUT RELEVANT DATA STRUCTURES: ###
Python lists are fine to use as LIFO queues (aka stacks).
You might consider the append() and pop() methods.
However, python lists don't implement FIFO Queues very efficiently.
A "deque" (double-ended queue) improve on lists in this regard.
Consider the append(), appendleft(), pop(), and popleft() methods
    https://docs.python.org/3/library/collections.html#collections.deque
A PriorityQueue implemention is provided for you - see priorityqueue.py.
It uses the heapq module to implement a heap. You don't need to understand
heaps to use PriorityQueue, but you can read more here:
    https://docs.python.org/3/library/heapq.html
When implementing a filter (aka graph search), it may be helpful to use the Set class.
Sets are like python dictionaries, except they only store keys.
The "in" keyword invokes a key lookup.
    https://docs.python.org/3/tutorial/datastructures.html#sets
"""


"""
RandWalk is a provided search "algorithm". Attempts to find a path to the goal state from initial_state.
If a solution is found, returns the final StateNode, from which the path can be found.
If search fails/terminates early, returns None.
state_callback_fn is called on every "extended" (visited) StateNode.
Search terminates early if state_callback_fn returns True.
Also updates the counter dict with the num_extends (how many states are extended)
and num_enqueues (how may states are added to the frontier)
You should implement the following options
1) avoid backtracking (if avoid_backtrack = True)
2) filter extended states (if filtering = True)
3) cutoff search early at a given depth (cutoff)
"""
def RandWalk(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}):

    frontier = [initial_state]

    extended_filter = set()

    while frontier: # frontier is False when it is empty. So just keep going until out of places to go...
        # choose next state to "extend" from frontier
        ext_node = random.choice(frontier)

        if (filtering and ext_node.get_all_features() in extended_filter):
            continue

        extended_filter.add(ext_node.get_all_features())

        counter['num_extends'] += 1

        # are we there? If so, return the node.
        if ext_node.is_goal_state():
            return ext_node

        # Update our caller (e.g. GUI) with the state we're extending.
        # Terminate search early if True is returned.
        if(state_callback_fn(ext_node)):
            break

        ### Update frontier with next states
        frontier = []
        for state in ext_node.generate_next_states():
            if (avoid_backtrack and ext_node.get_parent() == state):
                continue

            if (filtering and state.get_all_features() in extended_filter):
                continue

            if (cutoff != INF and state.get_path_length() > cutoff):
                continue

            frontier.append(state)
            counter['num_enqueues'] += 1

    # if loop breaks before finding goal, search is failure; return None
    return None

"""
Implement DFS, BFS, and UCS algorithms in a similar paradigm to the above.
You may find that all 3 are very similar...
Attempt to find a path to the goal state from initial_state.
If a solution is found, returns the final StateNode, from which the path can be found.
If search fails/terminates early, returns None.
state_callback_fn should be called on every "extended" (visited) StateNode.
Search should terminate early if state_callback_fn returns True.
Also updates the counter dict with the num_extends (how many states are extended)
and num_enqueues (how may states are added to the frontier)
You should implement the following options for each algorithm
1) avoid backtracking (if avoid_backtrack = True)
2) filter extended states (if filtering = True)
3) cutoff search early at a given depth (cutoff)
"""


def DFS(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}):

    frontier = [initial_state]

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

            frontier.append(state)
            counter['num_enqueues'] += 1

    # if loop breaks before finding goal, search is failure; return None
    return None

def BFS(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}):

    frontier = deque()

    frontier.append(initial_state)

    extended_filter = set()
    while frontier:  # frontier is False when it is empty. So just keep going until out of places to go...

        # choose next state to "extend" from frontier
        ext_node = frontier.popleft()


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

            frontier.append(state)
            counter['num_enqueues'] += 1

    # if loop breaks before finding goal, search is failure; return None
    return None


#Perform Uniform Cost Search
def UCS(initial_state, avoid_backtrack = False, filtering = False, cutoff = INF,
        state_callback_fn = lambda state : False, # A callback function for extended states. If it returns True, terminate
        counter = {'num_enqueues':0, 'num_extends':0}): # A counter for

    frontier = PriorityQueue()
    frontier.append(initial_state, initial_state.get_path_cost())

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

            frontier.append(state, state.get_path_cost())
            counter['num_enqueues'] += 1

    # if loop breaks before finding goal, search is failure; return None
    return None
# Lab 2: Games (Connect-4, Roomba Race)
# Name(s): Elias Cho, Arjun Nair
# Email(s): elicho21@bergen.org, arjnai21@bergen.org

from connectfour_gamestate import ConnectFourGameState
from tictactoe_gamestate import TicTacToeGameState
from nim_gamestate import NimGameState
from roomba_gamestate import RoombaRaceGameState
"""
In order to use any of the search methods in lab2_algorithms.py
you'll need define some utility functions and heuristic evaluation functions.
A few have been provided for you, and you can create as many additional ones as
you like (add to the game specific dict to show them on the GUI)
You MUST implement the following:
Part 1:
    basic_endgame_utility
    faster_endgame_utility
    win_paths_eval_tictactoe
Part 2:
    weighted_chains_eval_connectfour
Part 3:
    aggressive_eval_roomba
    defensive_eval_roomba
You MAY wish to implement the following to stretch your creativity:
    advanced_heuristic_eval_connectfour
    advanced_heuristic_eval_roomba
Some useful built-in python methods:
    any(list-like) - returns if at least one True
    all(list-like) - returns if all are True
    sum(list-like) - returns sum of all (??)
    listobj.count(item) - returns count of items in list
"""

### Part 1: Basic Utility Functions, TicTacToe #########################################

## General purpose evaluation functions: ###########

def basic_endgame_utility(state, maximizer_player_num):
    """ Given an endgame state and the player number of the "maximizer",
    returns utility 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie.
    """
    winner = state.endgame_winner()
    utility = ((winner + 1) % 3 - 1) * 1000
    if (maximizer_player_num == 2):
        utility *= -1
    return utility

def faster_endgame_utility(state, maximizer_player_num):
    """ Given an endgame state and the player number of the "maximizer",
    returns 0 in case of a tie, or a utility with abs(score) >= 1000,
    returning larger absolute scores for winning/losing sooner.
    This incentivizes winning more quickly, and losing later.
    """
    notEmpty = 0
    for y in range(state.num_rows):
        for x in range(state.num_cols):
            if state.board_array[y][x] != 0:
                notEmpty += 1
    return basic_endgame_utility(state, maximizer_player_num) / (notEmpty - 4)



def always_zero(state, maximizer_player_num):
    """ Always returns zero.
    Works as a dummy heuristic evaluation function for any situation.
    Truly useful heuristic evaluation functions must almost always be game-specific!
    """
    return 0


## Nim specific evaluation functions: ###########

def empty_rows_eval_nim(state, maximizer_player_num):
    """ Given a non-endgame NimGameState, estimate the value
    (expected utility) of the state from maximizer_player_num's view.
    Return the fraction of rows that are empty. The more empty rows, the better.
    This is not a zero-sum evaluation - both max and min get the same est. utility.
    Still, this can be helpful because usually forcing rows to empty is good.
    """
    return [state.get_stones_in_pile(p) for p in range(state.get_num_piles())].count(0) / state.get_num_piles()

nim_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                "empty rows": empty_rows_eval_nim}
}


## TicTacToe specific evaluation functions: ###########

## Edges are valued least, center valued highest.
space_values_tictactoe = {  (0,0):20, (0,1):10, (0,2):20,
                            (1,0):10, (1,1):30, (1,2):10,
                            (2,0):20, (2,1):10, (2,2):20}

def space_values_eval_tictactoe(state, maximizer_player_num):
    """ Given a non-endgame TicTacToeGameState, estimate the value
    (expected utility) of the state from maximizer_player_num's view.
    Return a linearly weighted sum of the "value" of each piece's position.
    Maximizer's pieces are + value, Minimizer's pieces are - value.
    """
    eval_score = 0
    for r in range(TicTacToeGameState.num_rows):
        for c in range(TicTacToeGameState.num_cols):
            piece = state.board_array[r][c]
            if piece == 0:
                continue
            elif piece == maximizer_player_num:
                eval_score += space_values_tictactoe[(r,c)]
            else:
                eval_score -= space_values_tictactoe[(r,c)]
    return eval_score

def win_paths_eval_tictactoe(state, maximizer_player_num):
    """ Given a non-endgame TicTacToeGameState, estimate the value
    (expected utility) of the state from maximizer_player_num's view.
    Return the difference in the number of possible winning paths for
    each player. More precisely:
    Return E(n) = M(n) - O(n)
    where M(n) is the total of Maximizer's possible winning lines
    O(n) is the total of Minimizer's possible winning lines.
    """

    value = 0
    opponent = 1 if maximizer_player_num == 2 else 2
    # Horizontal wins
    for r in range(state.num_rows):
        maxCount = 0
        minCount = 0
        for c in range(state.num_cols):
            if state.get_piece_at(r, c) == maximizer_player_num:
                maxCount += 1
            elif state.get_piece_at(r, c) == opponent:
                minCount -= 1
        if maxCount == 0 and minCount == 0:
            continue
        elif maxCount == 0:
            value -= 1
        elif minCount == 0:
            value += 1

    # Vertical wins
    for c in range(state.num_cols):
        maxCount = 0
        minCount = 0
        for r in range(state.num_rows):
            if state.get_piece_at(r, c) == maximizer_player_num:
                maxCount += 1
            elif state.get_piece_at(r, c) == opponent:
                minCount -= 1
        if maxCount == 0 and minCount == 0:
            continue
        elif maxCount == 0:
            value -= 1
        elif minCount == 0:
            value += 1

    # Diagonal down-right wins
    maxCount = 0
    minCount = 0
    for i in range(3):
        if state.get_piece_at(i, i) == maximizer_player_num:
            maxCount += 1
        elif state.get_piece_at(i, i) == opponent:
            minCount -= 1
    if maxCount == 0 and minCount != 0:
        value -= 1
    elif minCount == 0 and maxCount != 0:
        value += 1

    # Diagonal up-right wins
    maxCount = 0
    minCount = 0
    for i in range(3):
        if state.get_piece_at(2 - i, i) == maximizer_player_num:
            maxCount += 1
        elif state.get_piece_at(2 - i, i) == opponent:
            minCount -= 1
    if maxCount == 0 and minCount != 0:
        value -= 1
    elif minCount == 0 and maxCount != 0:
        value += 1

    # If you get here, no winner yet!
    return value

tictactoe_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                "space values": space_values_eval_tictactoe,
                                "win paths": win_paths_eval_tictactoe}
}

### Part 2 - Implement Connect Four ################################################

## Connect-four specific evaluation functions: ###########

def weighted_chains_eval_connectfour(state, maximizer_player_num):
    """
    Given a non-endgame ConnectFourGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.
    Utilizes the number of piece chains found for both players and makes a weighted
    sum to estimate value.
    """
    minimizer_player_num = 1 if maximizer_player_num == 2 else 2
    chain_sum_diff = 0
    # No need to count 4 because it would be endgame and eval_fn would not run
    for i in range(1, 4):
        chain_sum_diff += (state.get_num_chains(i, maximizer_player_num) - state.get_num_chains(i, minimizer_player_num)) * (i**2)

    return chain_sum_diff


def advanced_heuristic_eval_connectfour(state, maximizer_player_num):
    """
    Given a non-endgame ConnectFourGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.
    OPTIONAL
    """
    raise NotImplementedError
    return 0

connectfour_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                            "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                              "chains": weighted_chains_eval_connectfour,
                              "advanced": advanced_heuristic_eval_connectfour}
}

### Part 3 - Emergent Behaviours in Roomba Race ################################################

## Roomba Race specific evaluation functions: ###########

def aggressive_eval_roomba(state, maximizer_player_num):
    """
    Given a non-endgame RoombaRaceGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.
    The closer to the opponent, the better.
    """


    current_pos = state.get_position(maximizer_player_num)
    minimizer_player_num = 1 if maximizer_player_num == 2 else 2
    other_pos = state.get_position(minimizer_player_num)

     #get manhattan distance
    distance = abs(current_pos[0] - other_pos[0]) + abs(current_pos[1] - other_pos[1])
    distance = 100 * (1/distance) #invert so that smaller values are larger. multiply values so that not all values are low decimals
    return distance

def defensive_eval_roomba(state, maximizer_player_num):
    """ Given a non-endgame RoombaRaceGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.
    The safer, the better.
    """
    space = 0
    grid = state.get_grid()
    current_pos = state.get_position(maximizer_player_num)
    minimizer_player_num = 1 if maximizer_player_num == 2 else 2
    other_pos = state.get_position(minimizer_player_num)
    y, x = current_pos
    # East
    while x < len(grid[y]):
        if grid[y][x] != '.' or (y, x) == other_pos:
            break
        space += 1
        x += 1
    x = current_pos[1]

    # South
    while y < len(grid):
        if grid[y][x] != '.' or (y, x) == other_pos:
            break
        space += 1
        y += 1
    y = current_pos[0]

    # West
    while x >= 0:
        if grid[y][x] != '.' or (y, x) == other_pos:
            break
        space += 1
        x -= 1
    x = current_pos[1]

    # North
    while y >= 0:
        if grid[y][x] != '.' or (y, x) == other_pos:
            break
        space += 1
        y -= 1

    # Don't count position already at
    space -= 4

    return space

def advanced_heuristic_eval_roomba(state, maximizer_player_num):
    """
    Given a non-endgame RoombaRaceGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.
    OPTIONAL
    """
    raise NotImplementedError
    return 0


roomba_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                "aggressive": aggressive_eval_roomba,
                                "defensive": defensive_eval_roomba,
                                "advanced" : advanced_heuristic_eval_roomba}
}



## Dictionary mapping games to their appropriate evaluation functions. Used by the GUIs
all_fn_dicts = { RoombaRaceGameState: roomba_functions,
    ConnectFourGameState: connectfour_functions,
    TicTacToeGameState: tictactoe_functions,
    NimGameState: nim_functions}
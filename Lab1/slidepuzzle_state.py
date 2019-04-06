# Lab 1, Part 1: Uninformed Search.
# Name(s): Arjun Nair, Elias Cho

from statenode import StateNode

#### Lab 1, Part 1b: Problem Representation #################################################


# command to test: python lab1_part1_gui.py slidepuzzle test_puzzles/test_puzzle[##].txt
class SlidePuzzleState(StateNode):

    NEIGHBORING_STEPS = {(0,1): "East", (1,0): "South", (0, -1): "West", (-1,0): "North"}


    """
    A 'static' method that reads mazes from text files and returns
    a SlidePuzzleState which is an initial state.
    """
    # Override
    def readFromFile(filename):
        with open(filename, 'r') as file:
            grid = []
            grid_size = int(file.readline())
            empty = ()
            for y in range(grid_size):
                x = 0
                row = []
                for i in file.readline().split():
                    if i == "0":
                        empty = (y,x)
                    row.append(int(i))
                    x += 1
                assert (len(row) == grid_size)

                grid.append(tuple(row)) # list -> tuple makes it immutable, needed for hashing
            grid = tuple(grid) # grid is a tuple of tuples - a 2d grid!

            return SlidePuzzleState(gridSize=grid_size,
                                    grid=grid,
                                    last_action=None,
                                    parent=None,
                                    path_length=0,
                                    path_cost=0,
                                    empty_pos=empty)

    """
    Creates a SlidePuzzleState node.
    Takes:
        ADDITIONAL PARAMETERS OF YOUR DESIGN
    parent: the preceding StateNode along the path taken to reach the state
            (the initial state's parent should be None)
    path_length, the number of actions taken in the path to reach the state
    path_cost (optional), the cost of the entire path to reach the state
    """
    def __init__(self, gridSize, grid, last_action, parent, path_length, path_cost=0, empty_pos=None) :
        super().__init__(parent, path_length, path_cost)
        self.gridSize = gridSize
        self.grid = grid
        self.last_action = last_action
        self.empty_pos = empty_pos


    """
    Returns the dimension N of the square puzzle represented which is N-by-N.
    Needed by the GUI, should be FAST
    """
    def size(self):
        return self.gridSize

    """
    Returns the number at the tile at the given row and col (starting from 0).
    If the empty tile, return 0.
    Needed by the GUI, should be FAST
    """
    def tile_at(self, row, col) :
        return self.grid[row][col]

    """
    Returns a 2-tuple (row, col) of coordinates of the empty tile.
    Needed by the GUI, should be FAST
    """
    def get_empty_pos(self):
        return self.empty_pos


    """
    Returns a full feature representation of the environment's current state.
    This should be an immutable type - only primitives, strings, and tuples.
    (no lists or objects).
    If two StateNode objects represent the same state,
    get_features() should return the same for both objects.
    Note, however, that two states with identical features
    may have different paths.
    """
    # Override
    def get_all_features(self) :
        return self.empty_pos, self.grid

    """
    Returns True if a goal state.
    """
    # Override
    def is_goal_state(self) :
        counter = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] != counter:
                    return False
                counter += 1
        return True

    """
    Return a string representation of the State
    This gets called when str() is used on an Object.
    """
    # Override
    def __str__(self):
        strs = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                strs += str(self.grid[i][j]) + " "
            strs += "\n"
        return strs


    """
    Returns a string describing the action taken from the parent StateNode
    that results in transitioning to this StateNode
    along the path taken to reach this state.
    (None if the initial state)
    """
    # Override
    def describe_previous_action(self) :
        return self.last_action

    """
    Generate and return an iterable (e.g. a list) of all possible neighbor
    states (StateNode objects).
    If avoid_backtrack is True, don't include the parent state in the iterable.
    """
    # Override
    def generate_next_states(self) :
        states = []
        for dr, dc in SlidePuzzleState.NEIGHBORING_STEPS:
            new_x, new_y = self.empty_pos[0] + dr, self.empty_pos[1] + dc

            # Don't use any out-of-bounds moves
            if (new_x < 0) or (new_y < 0) or (new_x >= self.gridSize) or (new_y >= self.gridSize):
                continue
            # copy grid
            new_grid = [list(row) for row in self.grid]
            # switch positions
            tmp = new_grid[new_x][new_y]
            new_grid[new_x][new_y] = 0
            new_grid[self.empty_pos[0]][self.empty_pos[1]] = tmp
            tuple_new_grid = tuple([tuple(row) for row in new_grid])
            next_state = SlidePuzzleState(gridSize=self.gridSize,
                                          grid=tuple_new_grid,
                                          last_action=SlidePuzzleState.NEIGHBORING_STEPS[(dr, dc)],
                                          parent=self,
                                          path_length=self.path_length + 1,
                                          path_cost=self.path_length+1,
                                          empty_pos=(new_x, new_y)
                                          )

            states.append(next_state)
        return states

    """ You may add additional methods that may be useful! """
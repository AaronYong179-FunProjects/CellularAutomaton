import random
import numpy as np
import copy
import cv2

# https://robertheaton.com/2018/07/20/project-2-game-of-life/

#####################################
## Random soup generator functions ##
#####################################

def init_state(width, height):
    return np.zeros((height, width))

def random_state(width, height):
    """ Creates a random soup of life.

    Each cell has a 50% probability of spawning with life. 
    """
    state = init_state(width, height)
    for row in range(height):
        for col in range(width):
            rand = random.random()
            state[row,col] = 1 if rand >= 0.50 else 0
    return state

###############################################
## Rulesets determining cell neighbour count ##
###############################################

def get_neighbour_count(index, state, fn):
    """ General "live" neighbour counting function.
    
    The exact definition of a "neighbour" will be handled by
    a function passed into :param: `fn`
    """
    neighbours = fn(index, state)
    return sum(map(lambda x: state[x[0], x[1]], neighbours))

def get_neighbours_Moore(index, state):
    """ Returns the coordinates all cells in a Moore neighbourhood. 
    
    The Moore neighbourhood is defined as the eight cells surronding a 
    central cell.
    """
    row, col = index
    height, width = state.shape
    neighbours = []
    for row_shift in range(-1, 2):
        for col_shift in range(-1, 2):
            if row_shift == col_shift == 0:
                continue
            neighbours.append(
                ((row + row_shift) % height, (col + col_shift) % width)
            )
    return neighbours

#######################################
## Rulesets determining fate of cell ##
#######################################

def game_of_life_ruleset(state, coord, neighbour_count):
    """ Determines the fate of a cell at :param: `coord` based
    on the Game of Life ruleset.
    
    The rules are:
    i) Any live cell with < two neighbours dies by underpopulation
    ii) Any live cell with > three neighbours dies by overpopulation
    iii) Any live cell with two or three neighbours survives
    iv) Any dead cell with exactly three neighbours becomes a live cell

    ! This is an impure function, the input state will be mutated.
    Nothing is returned by this function ! 
    """
    cell = state[coord]

    if cell and (neighbour_count < 2 or neighbour_count > 3):
        state[coord] = 0
    elif not cell and neighbour_count == 3:
        state[coord] = 1

RULEBOOK = {
    "game_of_life" : 
    {
        "neighbour_count":  get_neighbours_Moore,
        "ruleset": game_of_life_ruleset
    }
}

############################################
## Functions in charge of running the sim ##
############################################

def calc_next_state(state, rule):
    """ Calculates the next state given the cellular automaton variant used.

    Cellular automatons implemented here differ in two main areas: 
    1. rules regarding which adjacent cells are considered "neighbours"
    2. rules regarding which cells will die/survive/spawn

    These rules will be pulled from the global dictionary RULEBOOK.

    The next state is returned without mutating the original input state.
    """

    # extract celular automaton rules
    count_fn = RULEBOOK[rule]["neighbour_count"]
    ruleset_fn = RULEBOOK[rule]["ruleset"]

    next_state = copy.deepcopy(state)
    height, width = state.shape

    # for each cell, apply celular automaton rules
    for row in range(height):
        for col in range(width):
            count = get_neighbour_count((row, col), state, count_fn)
            ruleset_fn(next_state, (row, col), count)

    return next_state

def read_pattern(directory, board_size):
    """ Reads a pattern from a text file and pads the pattern to :param: `board_size`. """
    pattern = np.loadtxt(directory)
    pattern_height, pattern_width = pattern.shape

    pad_width = board_size - pattern_width
    pad_height = board_size - pattern_height

    pattern = np.pad(pattern, [(0, pad_height), (0, pad_width)] ,constant_values=0)
    return pattern

def render(state, refresh_rate):
    """ Renders the current state, refreshing at a given refresh rate.

    States are resized (10x magnification) just for viewing purposes,
    using open-cv's nearest-neighbour interpolation.    
    """
    width, height = state.shape 
    state = cv2.resize(state, (width*10, height*10), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("sim", state)
    return cv2.waitKey(refresh_rate)

def run_sim(sim_name, size=50, refresh_rate=100, pattern=None):
    """ Runs the desired cellular automaton simulation. 

    Patterns can be loaded from .txt files as well.
    """

    if pattern is None:
        state = random_state(size, size)
    else:
        state = read_pattern(pattern, size)

    while True:
        key_press = render(state, refresh_rate)
        # press the 'q' key to stop the simulation
        if key_press == ord("q"):
            cv2.destroyAllWindows() # just for cleanliness sake
            break
        state = calc_next_state(state, sim_name)

run_sim("game_of_life", refresh_rate=75)

    
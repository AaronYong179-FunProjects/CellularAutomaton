import random
import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2

# https://robertheaton.com/2018/07/20/project-2-game-of-life/

def init_state(width, height):
    return np.zeros((height, width))

def random_state(width, height):
    state = init_state(width, height)
    for row in range(height):
        for col in range(width):
            rand = random.random()
            state[row,col] = 1 if rand >= 0.50 else 0
    return state
    
def render(state, refresh_rate):
    width, height = state.shape 
    state = cv2.resize(state, (width*10, height*10), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("sim", state)
    return cv2.waitKey(refresh_rate)

def get_neighbours_Moore(index, state):
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

def get_neighbour_count(index, state, fn):
    neighbours = fn(index, state)
    return sum(map(lambda x: state[x[0], x[1]], neighbours))

def game_of_life_ruleset(state, coord, neighbour_count):
    # impure function, mutates the state
    cell = state[coord]
    if cell and (neighbour_count <= 1 or neighbour_count > 3):
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

def calc_next_state(state, rule):

    count_fn = RULEBOOK[rule]["neighbour_count"]
    ruleset_fn = RULEBOOK[rule]["ruleset"]

    next_state = copy.deepcopy(state)
    height, width = state.shape
    for row in range(height):
        for col in range(width):
            count = get_neighbour_count((row, col), state, count_fn)
            ruleset_fn(next_state, (row, col), count)

    return next_state

def run_sim(sim_name, size=50, refresh_rate=100):

    state = random_state(size, size)

    while True:
        key_press = render(state, refresh_rate)
        if key_press == ord("q"):
            break
        state = calc_next_state(state, sim_name)

run_sim("game_of_life", refresh_rate=75)


    
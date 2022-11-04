# CellularAutomaton
A Pythonic cellular automaton implementation.

---
## cellular_automaton.py
_"A cellular automaton is a collection of cells arranged in a grid ... such that each cell changes state as a function of time, according to a defined set of rules driven by the states of the neighbouring cells. ([From TechTarget](https://www.techtarget.com/searchenterprisedesktop/definition/cellular-automaton))"_

The three main points of considerations for a cellular automaton are (arguably):
1. The state of any given cell
2. The rules governing state changes of any cell
3. The definition of "neighbouring" cells

In this implementation of a general cellular automaton, the state of any given cell can only take values 0 or 1 (i.e., ON or OFF). Two rulesets governing the state changes of cells are implemented as a simple proof of concept; namely, the [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life) ruleset and the [Day and Night](https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)) ruleset. Finally, two definitions of "neighbouring" cells are given, the [Moore neighbourhood](https://en.wikipedia.org/wiki/Moore_neighborhood) and the [Von Neumann neighbourhood](https://en.wikipedia.org/wiki/Von_Neumann_neighborhood). These different rulesets can be toggled at the command line during the execution of the Python script.

Periodic boundary conditions are used, which assumes that edges of the game board wrap around to the opposite edge.

An example run of Conway's Game of Life using Moore neighbourhood (50 generations), is shown below:
`python3 ./cellular_automaton.py`

![](https://github.com/AaronYong179-FunProjects/CellularAutomaton/blob/main/img/GoLDemo.gif)

Patterns contained within a `.txt` file can be loaded into the simulation as well. A few files with sample patterns are located in the `/patterns/` folder.

An example of a [glider](https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)) is shown below:

`python3 ./cellular_automaton.py -p "./patterns/glider.txt"`

![](https://github.com/AaronYong179-FunProjects/CellularAutomaton/blob/main/img/gliderDemo.gif)

A much more impressive example is the [Gosper Glider Gun](https://conwaylife.com/wiki/Gosper_glider_gun), spawning two gliders within 50 generations.

`python3 ./cellular_automaton.py -p "./patterns/gosper_glider_gun.txt"`

![](https://github.com/AaronYong179-FunProjects/CellularAutomaton/blob/main/img/gggDemo.gif)

A final example, a rocket ship from the [Day and Night](https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)) cellular automaton:

`python3 ./cellular_automaton.py -rc "day_and_night" -p "./patterns/rocket_ship.txt"`

![](https://github.com/AaronYong179-FunProjects/CellularAutomaton/blob/main/img/rocketDemo.gif)

#### Notes
Written with Python 3.10.4.
External library used:
- opencv (`pip install opencv-python`)

---

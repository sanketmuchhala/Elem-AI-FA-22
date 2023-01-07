#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: Sakshi Rathi sakrathi@iu.edu
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys
from queue import PriorityQueue
N = 5

#####
# THE ABSTRACTION:
# In solve,converted fringe to a priority queue.
# the priority of every state is the evaluation function f(s)
# which is equal to g(s) + h(s)
# where g(s) is the cost of path of current state to the initial state and h(s) is the heuristic of the current state.
# the heuristic is the number of misplaced elements in the list when compared to the goal state.

# Initial state:
# Goal state:
# given a state, returns True or False to indicate if the current state is the goal state
def is_goal(state):
    return state == list(range(1, N + 1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [state[0:n] + [state[n + 1], ] + [state[n], ] + state[n + 2:] for n in range(0, N - 1)]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
# heuristic to calculate misplaced elements when compared to goal state
def h(state):
    n = 0 #the count of misplaced numbers/tiles
    i = 0 #the increament counter to for the ordered placement that is 1 to N, i being increamented from 1 to N
    for ele in state:
        i += 1
        if ele != i:
            n += 1
    return n
#########
#
# THE ALGORITHM:
#
# implementing astar search algorithm.
#
def solve(initial_state):
    fringe = PriorityQueue()
    fringe.put(((initial_state, []),h(initial_state)))
    g  = 0 #cost of initial state to current state
    while not fringe.empty():
        ((state, path),heu) = fringe.get()
        g = g + 1

        if is_goal(state):
            return path + [state, ]

        for s in successors(state):
            gs = g + 1 #cost of path of initial state to current state
            f = gs + h(s)
            fringe.put(((s, path + [state, ]),f ))

    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise (Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([int(i) for i in line.split()])

    for initial_state in test_cases:
        print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

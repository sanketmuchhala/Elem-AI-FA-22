#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
import numpy as np

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    allSucc = []
    for row in range(1,ROWS+1):
      allSucc += [(move_board(state.copy(), "R"+str(row)), "R"+str(row))]
      allSucc += [(move_board(state.copy(), "L"+str(row)), "L"+str(row))]

    for col in range(1,COLS+1):
      allSucc += [(move_board(state.copy(), "U"+str(col)), "U"+str(col))]
      allSucc += [(move_board(state.copy(), "D"+str(col)), "D"+str(col))]

    allSucc += [(move_board(state.copy(), "Ic"), "Ic")]
    allSucc += [(move_board(state.copy(), "Oc"), "Oc")]
    allSucc += [(move_board(state.copy(), "Icc"), "Icc")]
    allSucc += [(move_board(state.copy(), "Occ"), "Occ")]

    return allSucc

    return allSucc

def move_board(state, instr):
  fst = instr[0]
  lst = instr[1:]
  if fst == "R":
    pos = int(lst)-1 #get the row index
    row = state[pos] #get the row
    rRow = np.roll(row, 1) #add the row to the last val
    state[pos] = rRow #add the row to the state
    return state
  elif fst == "L":
    pos = int(lst)-1 #get the row index
    row = state[pos] #get the row
    lRow = np.roll(row, -1) #add the row to the last val
    state[pos] = lRow #add the row to the state
    return state

  elif fst == "U":
    pos = int(lst)-1 #get the row index 
    col = state[:,pos] #get the col
    lCol = np.roll(col, -1) #add the col to the last val
    state[:,pos] = lCol #add the col to the state
    return state
  elif fst == "D":
    pos = int(lst)-1 #get the row index 
    col = state[:,pos] #get the col
    lCol = np.roll(col, 1) #add the col to the last val
    state[:,pos] = lCol #add the col to the state
    return state

  elif fst == "I":
    innerMatrix = state[1:ROWS-1,1:COLS-1]
    if lst == "c": #clockwise
      innerMatrix[0] = np.roll(innerMatrix[0],1)
      innerMatrix[:,0] = np.roll(innerMatrix[:,0],-1)
      innerMatrix[2] = np.roll(innerMatrix[2],-1)
      innerMatrix[1,2], innerMatrix[2,2] = innerMatrix[2,2], innerMatrix[1,2]
      state[1:ROWS-1,1:COLS-1] = innerMatrix
      return state
    elif lst == "cc": #Counter clockwise
      innerMatrix[:,2] = np.roll(innerMatrix[:,2],-1)
      innerMatrix[2] = np.roll(innerMatrix[2],1)
      innerMatrix[:,0] = np.roll(innerMatrix[:,0],1)
      innerMatrix[0,0], innerMatrix[0,1] = innerMatrix[0,1], innerMatrix[0,0]
      state[1:ROWS-1,1:COLS-1] = innerMatrix
      return state
  elif fst == "O": 
    if lst == "c": #clockwise
      state[0] = np.roll(state[0],1)
      state[:,0] = np.roll(state[:,0],-1)
      state[4] = np.roll(state[4],-1)
      state[1:,4] = np.roll(state[1:,4],1)
      return state
    elif lst == "cc": #Counter clockwise
      state[:,4] = np.roll(state[:,4],-1)
      state[4] = np.roll(state[4],1)
      state[:,0] = np.roll(state[:,0],1)
      state[0][:4] = np.roll(state[0][:4],-1)
      return state
  else:
    print("Not a valid command")

def convert_to_array(init_board):
  board = []
  for row in range(0,ROWS*COLS, 5):
    board.append(list(init_board[row:row+5]))
  return board

# check if we've reached the goal
def is_goal(state):
  finalPos = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])
  return np.array_equiv(state, finalPos)

def h(state):
  finalPos = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])
  boolAr = finalPos==state

  herMatrix = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
  her = 0
  for row in range(len(boolAr)):
    for col in range(len(boolAr[row])):
      if boolAr[row][col]==False:
        val = finalPos[row][col]
        x,y = np.where(state== val)

        temp = abs(row-x)
        if temp == 4: #if the dist is 4 you know it wraps
          herMatrix[row][col] += 1
        elif temp == 3: #if the dist is 3 you know it wraps
          herMatrix[row][col] += 2
        else:
          herMatrix[row][col] += temp
        
        temp = abs(col-y)
        if temp == 4:
          herMatrix[row][col] +=1
        elif temp == 3:
          herMatrix[row][col] +=2
        else:
          herMatrix[row][col] +=temp
  
  #Subtract for the rows and cols with all the same dist
  for row in herMatrix:
    if len(set(row)) == 1:
      her-=10

  for i in range(COLS):
    col = state[:,i]
    if len(set(col)) == 1:
      her-=10

  her += np.sum(herMatrix)

  return her

def solve(initial_board):
  """
  1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
  2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
      For testing we will call this function with single argument(initial_board) and it should return 
      the solution.
  3. Please do not use any global variables, as it may cause the testing code to fail.
  4. You can assume that all test cases will be solvable.
  5. The current code just returns a dummy solution.
  """

  #make the board a np array
  board = np.array(convert_to_array(initial_board))

  #make a copy of the initial board to compare to
  init_board = board.copy()

  #make the fringe and add the initial board to it
  fringe = []
  fringe.append((0, (board, [])))

  while len(fringe) > 0:
    (cost, (state, path)) = fringe.pop(0) #get the first val

    if is_goal(state):
        return path
    
    for s, move in successors(state):
        newCost = h(s) + cost
        newState = (s, path + [move])
        fringe.append((newCost, newState))

    fringe = sorted(fringe, key=lambda tup: tup[0])


  return ["Oc","L2","Icc", "R4"]

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))

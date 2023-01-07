# misere_ttt.py

import random

# default is a 4x4 board -- you can change this
ROWS = 3
COLS = ROWS

### these are helper functions
def transpose_board(board):
    return [list(col) for col in zip(*board)]

def is_any_row_full(board):
    return ["x"] * COLS in board

def is_any_col_full(board):
    return ["x"] * COLS in transpose_board(board)

def is_any_diag_full(board):
    return is_any_row_full([[board[i][i] for i in range(0,ROWS)], [board[i][COLS-i-1] for i in range(0,ROWS)]])

def board_to_string(board):
    return "  " + " ".join([str(b) for b in range(0,COLS)]) + "\n" + \
        "\n".join([chr(r+ord('a')) + " " + " ".join(board[r]) for r in range(0,ROWS)])

### check if the current board has any row, col, or diag complete
def check_win(board):
    return is_any_row_full(board) or is_any_col_full(board) or is_any_diag_full(board)

### add a piece to the board, returning a new copy of the board (not updating existing board)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + ["x",] + board[row][col+1:]] + board[row+1:]

### code to get a human-entered move
def get_human_move(board):
    move = input('Please enter where you want to place a tile (in a format like a1): ')
    (r, c) = ((ord(move[0]) - ord('a')), int(move[1]))
    while((not (0 <= r < ROWS and 0 <= c <= COLS)) or board[r][c] == 'x'):
        print('Invalid move!')
        move = input('Please enter where you want to place a tile (in a format like a1): ')
        (r, c) = ((ord(move[0]) - ord('a')), int(move[1]))
        
    return (r,c)

### code to get an AI move
# for right now, this code just returns a random move.
# This is where you'll want to implement minimax!!
#
def get_ai_move(board):
    return minimax(board)[0]

def minimax(board):
    move = (0,0)
    best = -2
    if check_win(board): # if we've won, that's the best, so score = 1
        return (None,1)
    else: # if we haven't won, look at all possible moves
        for r in range(0,ROWS):
            for c in range(0,COLS):
                if board[r][c] == 'x': continue # Soren: if the code can place 'x's on already occupied spaces, it will
                  # enter an endless loop of trying to evaluate a board by placing 'x's on the first square- so we don't
                  # allow it to place 'x's if the space is occupied
                new_board = add_piece(board,r,c) # define the board
                compare = -1*minimax(new_board)[1] # we want the opposite of our opponent, so *-1
                if compare == 1: # simplified alpha-beta pruning (we can't use the whole algorithm, since our only values are 1 and -1 atm)
                    return ((r,c), 1)
                if compare > best: # maintaining the best value so far
                    best = compare
                    move = (r,c)
    return (move, best)

### Main program!

# create initial empty board
board = [ ["."] * COLS for i in range(0, ROWS) ]
print(board_to_string(board))

while True:
    (r,c) = get_human_move(board)
    board = add_piece(board, r, c)
    print("-- New board after human move:\n" + board_to_string(board))
    if(check_win(board)):
        print("AI won!!")
        break
    
    (r,c) = get_ai_move(board)
    board = add_piece(board, r, c)
    print("-- New board after AI move:\n" + board_to_string(board))
    if(check_win(board)):
        print("Human won!!")
        break

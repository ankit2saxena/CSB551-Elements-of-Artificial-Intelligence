#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Ankit Saxena, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.kit

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 


# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 


# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )


# Check (locked_x, locked_y) is not occupied
def check_locked(board):
    if locked_x == 0 and locked_y == 0:
        return True
    else:
        return board[locked_x - 1][locked_y - 1] != 1
    

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    if flag:
        return "\n".join([ " ".join([ 'X' if (row == locked_x-1 and col == locked_y-1 and not board[row][col] and locked_x >= 1 and locked_y >= 1) 
                                 else '_' if not board[row][col] 
                                 else 'R' if prob_type == 'nrook' else 'Q'
                                 for col in range(0, N - 1) ]) for row in range(0, N - 1) ])
    else:
        return "\n".join([ " ".join([ 'X' if (row == locked_x-1 and col == locked_y-1 and not board[row][col] and locked_x >= 1 and locked_y >= 1) 
                                 else '_' if not board[row][col] 
                                 else 'R' if prob_type == 'nrook' else 'Q'
                                 for col in range(0, N) ]) for row in range(0, N) ])


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]


# Get list of successors of given board state
def successors(board):
    temp = []
    for r in range(0, N):
        for c in range(0, N):
            
            if count_on_row(board, r) < 1 and count_on_col(board, c) < 1:
                sample = add_piece(board, r, c)
                
                if check_locked(sample):
                    if prob_type == 'nrook' and \
                            all( [ count_on_row(sample, r) <= 1 for r in range(0, N) ] ) and \
                            all( [ count_on_col(sample, c) <= 1 for c in range(0, N) ] ):
                        temp.append(sample)
                        
                    if prob_type == 'nqueen' and \
                            all( [ count_on_row(sample, r) <= 1 for r in range(0, N) ] ) and \
                            all( [ count_on_col(sample, c) <= 1 for c in range(0, N) ] ) and \
                            check_diag(sample):
                        temp.append(sample)
                        
                
    return temp


# Check the diagonals for n-queens problem
def check_diag(board):
    
    if flag and board[N - 1][N - 1] != 1:
        return False
    
    sum_diag_1 = [0]*(2 * N)
    sum_diag_2 = [0]*(2 * N)
    
    for i in range(0, N):
        for j in range(0, N):
            summ = i + j
            diff = i - j
            
            if diff < 0:
                diff = N - 1 - diff
            
            if board[i][j] == 1:
                sum_diag_1[(diff)] = sum_diag_1[(diff)] + 1
                sum_diag_2[(summ)] = sum_diag_2[(summ)] + 1
                
            if sum_diag_1[(diff)] > 1 or sum_diag_2[(summ)] > 1:
                return False
        pass
    pass

    for k in range((2 * N)):
        if sum_diag_1[k] > 1 or sum_diag_2[k] > 1:
            return False
    
    return True


# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N


# Solve n-rooks and n-queens
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors( fringe.pop() ):
            if is_goal(s):
                    return(s)

            fringe.append(s)
    return False

#input the command line arguments
prob_type = sys.argv[1]
N = int(sys.argv[2])
locked_x = int(sys.argv[3])
locked_y = int(sys.argv[4])

flag = False

# check if valid unavailable squares are provided.
if locked_x < 0 or locked_y < 0 or locked_x > N or locked_y > N:
    print 'Please enter valid values for unavailable squares.'
    exit()

# check if a valid problem type is provided.
if prob_type == 'nrook' or prob_type == 'nqueen':
    
    if prob_type == 'nqueen' and N % 2 != 0 and N >= 15:
        flag = True
        N = N + 1

    initial_board = [[0]*N]*N

    #print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
    solution = solve(initial_board)
    print (printable_board(solution) if solution else "Sorry, no solution found. :(")
    
else:
    print 'Please enter a valid problem type.'
    exit()
    
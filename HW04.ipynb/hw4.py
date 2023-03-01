import numpy as np

# Board is 8x8 numpy array
# 0 = no piece
# 1 = X piece
# 2 = O piece

blank = 0
X = 1
O = 2

symbol = [' ','X','O']

N = 8      

def getEmptyBoard():                              # use this function to create a fresh empty board
    return np.zeros((N,N)).astype(int)

# This will be used to indicate an error when you try to make a move in a column that is already full

ERROR = -1

# Check for error: use this function ONLY, since numpy arrays work strangely with comparisons

def isError(B):
    if type(B) == int:
        return B == ERROR
    else:
        return False

# Print out a human-readable version of the board, can indent if want to trace through the recursion

def printBoard(B,ind=0):
    indent = '\t'*ind
    if isError(B):
        print(indent,"ERROR: Overflow in column.")
        return
    print(indent,'  0 1 2 3 4 5 6 7')
    print(indent,'-------------------')
    for row in range(N):
        print(indent,'|',end='')
        for col in range(N):
            print(' '+ symbol[B[row][col]],end='')
        print(' |')
    print(indent,'-------------------')
    
# printBoard(getEmptyBoard())
# print()
# printBoard(ERROR)

# This function should make the indicated move on the input board, and return that board, or ERROR (-1)
# if there is no room in the column of the move.  Note that you are changing the original board
# IN PLACE, but also returning it, so you can indicate the error by returning ERROR (-1).
# Do NOT make a copy, as that is very inefficient!

# player is 1 (X) or 2 (O); 0 <= move <= 7; board is 8x8 numpy array as shown in first code cell.
# If move is illegal (either outside range 0..7) or there is no room in that column, return ERROR

def illegalMove(m):
    return not(0 <= m <= 7)

def noRoomInColumn(move,board):
    return board[0][move] != blank

def dropPiece(player,move,board):
    if illegalMove(move):
        return ERROR
    if noRoomInColumn(move,board):
        return ERROR
    for row in range(N - 1, 0, -1):
        if board[row][move] == blank:
            board[row][move] = player
            return board
    return board                     # just to get it to compile, you must write this function


# tests

# makeExample takes a list of X,O,X,O etc. moves and create a board. 
# May be useful for testing.  

def makeExample(moves):
    B = getEmptyBoard()
    player = X
    nextPlayer = O
    for m in moves:
        B = dropPiece(player,m,B) 
        if isError(B):               # NOTE: This is the way to check for an error return!
            return ERROR
        player,nextPlayer = nextPlayer,player
    return B


# Test out of range error -- See Appendix for what you should produce

# if(dropPiece(X,100,getEmptyBoard())):
#     print("Move outside range 0..7!")
# else:
#     print("Range test did not work. ")    
# print()

# # Test dropPiece

# B = dropPiece(X,3,getEmptyBoard())
# B = dropPiece(O,4,B)
# B = dropPiece(X,0,B)
# B = dropPiece(O,7,B)
# B = dropPiece(X,5,B)
# B = dropPiece(O,3,B)
# B = dropPiece(X,4,B)
# B = dropPiece(O,5,B)
# B = dropPiece(X,5,B)
# printBoard(B)
# print()


# L2R = list(range(8))
# R2L = L2R[::-1]
# M = (L2R + R2L) * 4


# fullBoard = makeExample(M)
# printBoard(fullBoard)
# print()


# # next one should return error message for any 0 <= m <= 7, since there is no room in any column

# m = 4

# print("No room in column "+str(m)+":",noRoomInColumn(m,fullBoard),'\n')

# printBoard( dropPiece(X,m,fullBoard) )

# player = 1 (X) or 2 (O)
# checkWin(X,board) returns X=1 if X wins,  else 0
# checkWin(O,board) returns O=2 if O wins,  else 0 

# No need to check if X and O both have winning sequences, since this will be used after each move.

def checkWin(player,board):    
    # check rows for four in a row
    for row in range(N):
        for col in range(N-3):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return player
    # check columns for four in a row
    for col in range(N):
        for row in range(N-3):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return player
    # check diagonals for four in a row
    for row in range(N-3):
        for col in range(N-3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return player
    for row in range(N-3):
        for col in range(N-3):
            if board[row][col+3] == player and board[row+1][col+2] == player and board[row+2][col+1] == player and board[row+3][col] == player:
                return player
    return 0

### Interactive version

# This last part of Problem One will enable you to play interactively against a random player. You should play the game sufficiently to understand the rules and some basic strategy before starting on the minmax version of the player.

# Since I/O is always the most frustrating and least interesting part of any program, the template below provides some basic interaction to build on.

# You should provide an interaction approximately as shown in the Appendix at the bottom of this notebook.

# Note carefully:

# You must check for a win after each move;

# Code your main loop as a for loop with a maximum of 64, so that if the board were to fill up, the game would terminate with the message "Tie game!" (just check if the for loop variable == 64 after the loop ends);

# Terminate the game with an appropriate error message (as shown in the Appendix) if your move is an error, i.e.,

# Move is not in the range 0..7; or
# Move is in a column that is already full.
# Note that the random player will never make an illegal move.

# The graders will play your game to verify that it works as expected.

from numpy.random import randint

def randomPlayer(board):
    m = randint(8)
    while noRoomInColumn(m,board):                # no move in this column, try again
        m = randint(8)                            
    return m

# following is just to show how to accept input from keyboard, you will rewrite all of this

# print("Welcome to Connect Four!")

# board = getEmptyBoard()
# printBoard(board)

# turn = True

# for i in range(64):
#     if turn:
#         print("Your move: ",end='')
#         move = int(input())
#         board = dropPiece(X,move,board)
#         if isError(board):
#             print("Illegal move!")
#             break
#         printBoard(board)
#         if checkWin(X,board):
#             print("You win!")
#             break
#     else:
#         print("Random Bot move: ",end='')
#         move = randomPlayer(board)
#         board = dropPiece(O,move,board)
#         if isError(board):
#             print("Illegal move!")
#             break
#         printBoard(board)
#         if checkWin(O,board):
#             print("You lose!")
#             break
#     print()
#     turn = not turn

# print("Bye!")

# PROBLEM 2

import sys

OWIN = sys.maxsize
XWIN = -OWIN

THREE_SCORE = 50                  # just for testing, you may want to experiment with different values
TWO_SCORE = 10                    # for these two parameters


# Return evaluation of the board from O's point of view


def eval(board):
    def count_score(seq):
        if seq.count(1) == 4:
            return XWIN
        elif seq.count(2) == 4:
            return OWIN
        elif seq.count(0) == 2 and seq.count(2) == 2:
            return TWO_SCORE
        elif seq.count(0) == 1 and seq.count(2) == 3:
            return THREE_SCORE
        elif seq.count(0) == 2 and seq.count(1) == 2:
            return -TWO_SCORE
        elif seq.count(0) == 1 and seq.count(1) == 3:
            return -THREE_SCORE
        else:
            return 0

    score = 0

    # Check rows
    for row in board:
        for i in range(len(row) - 3):
            seq = row[i:i+4]
            score += count_score(seq.tolist())

    # Check columns
    for j in range(len(board[0])):
        for i in range(len(board) - 3):
            seq = [board[i+k][j] for k in range(4)]
            score += count_score(seq)

    # Check diagonal (top-left to bottom-right)
    for i in range(len(board) - 3):
        for j in range(len(board[0]) - 3):
            seq = [board[i+k][j+k] for k in range(4)]
            score += count_score(seq)

    # Check diagonal (top-right to bottom-left)
    for i in range(len(board) - 3):
        for j in range(3, len(board[0])):
            seq = [board[i+k][j-k] for k in range(4)]
            score += count_score(seq)

    return score

# Code for Part B

maxNodeLimit = 10000           # You can not change this
maxDepth = 3                   # You will want to change this and experiment with different values

countNodes = 0

def get_valid_moves(board):
    valid_moves = []
    for col in range(N):
        if not noRoomInColumn(col, board):
            valid_moves.append(col)
    return valid_moves

def minMax(board, player, depth, alpha, beta):
    global countNodes
    countNodes += 1  
    
    if countNodes > maxNodeLimit or depth == maxDepth:
        score = eval(board)
        return (score, None)
    
    winner = checkWin(player, board)
    if winner != 0:
        score = eval(board)
        return (score, None)

    if player == O:
        best_score = -sys.maxsize
    else:
        best_score = sys.maxsize

    best_move = None

    for move in get_valid_moves(board):
        new_board = dropPiece(player, move, np.copy(board))
        score, _ = minMax(new_board, X, depth+1, alpha, beta)
        if player == O:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
        if beta <= alpha:
            break
    
    return (best_score, best_move)

    if player == O:  # maximizing player
        best_score = -sys.maxsize
        best_move = None
        for move in get_valid_moves(board):
            new_board = dropPiece(player, move, np.copy(board))
            score, _ = minMax(new_board, X, depth+1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return (best_score, best_move)
    
    else:  # minimizing player
        best_score = sys.maxsize
        best_move = None
        for move in get_valid_moves(board):
            new_board = dropPiece(player, move, np.copy(board))
            score, _ = minMax(new_board, O, depth+1, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return (best_score, best_move)

    
    
# You will use this function in your interactive version below

def player(board):    
    (_,move) = minMax(board,O,0,-sys.maxsize,sys.maxsize)    # only place we need the move
    return move

# tests for minimax

# Some simple tests:  better testing can be done by running the interactive version from Part C
# Your results may vary slight from what is shown here, but should be similar

maxDepth = 1          # minMax will call eval on all children of root node

board1 = makeExample([3,4,2,5,2,6,2])
# print()
# printBoard(board1)
print("minMax:", minMax(board1,O,0,-sys.maxsize,sys.maxsize) )  # (9223372036854775807, 7)

# board2 = makeExample([3,4,2,5,2,0,2])
# print()
# printBoard(board2)
# print("minMax:", minMax(board2,O,0,-sys.maxsize,sys.maxsize) )  # (10, 2)

# maxDepth = 2 

# board2 = makeExample([3,4,2,5,2,0,2])
# print()
# printBoard(board2)
# print("minMax:", minMax(board2,O,0,-sys.maxsize,sys.maxsize) )  # (-50, 2)

# board3 = makeExample([3,0,4,4,3,4,5])
# print()
# printBoard(board3)
# print("minMax:", minMax(board3,O,0,-sys.maxsize,sys.maxsize) )  # (-9223372036854775807, 7) every move loses!
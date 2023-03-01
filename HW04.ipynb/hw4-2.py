# Solution for Problem Three
# Your name: Jakob Brattke




# your code here
import numpy as np
import sys

# board constants
blank = 0
X = 1
O = 2
N = 8
ERROR = -1

# eval constants
OWIN = sys.maxsize
XWIN = -OWIN
THREE_SCORE = 50
TWO_SCORE = 10

# minimax constants
maxNodeLimit = 10000
maxDepth = 5
countNodes = 0

# ----------- board methods -----------
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
    return board 

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

# ----------- eval methods -----------
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

def eval(board):
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


# ----------- Minimax methods -----------
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

def player(board):    
    (_,move) = minMax(board,O,0,-sys.maxsize,sys.maxsize)    # only place we need the move
    return move


# ----------- tests -----------
def isError(B):
    if type(B) == int:
        return B == ERROR
    else:
        return False
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
def getEmptyBoard():                              # use this function to create a fresh empty board
    return np.zeros((N,N)).astype(int)
symbol = [' ','X','O']
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

maxDepth = 1          # minMax will call eval on all children of root node

board1 = makeExample([3,4,2,5,2,6,2])
print()
printBoard(board1)
print("minMax:", minMax(board1,O,0,-sys.maxsize,sys.maxsize) )  # (9223372036854775807, 7)

board2 = makeExample([3,4,2,5,2,0,2])
print()
printBoard(board2)
print("minMax:", minMax(board2,O,0,-sys.maxsize,sys.maxsize) )  # (10, 2)

maxDepth = 2 

board2 = makeExample([3,4,2,5,2,0,2])
print()
printBoard(board2)
print("minMax:", minMax(board2,O,0,-sys.maxsize,sys.maxsize) )  # (-50, 2)

board3 = makeExample([3,0,4,4,3,4,5])
print()
printBoard(board3)
print("minMax:", minMax(board3,O,0,-sys.maxsize,sys.maxsize) )  # (-9223372036854775807, 7) every move loses!
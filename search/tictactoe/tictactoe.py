"""
Tic Tac Toe Player
"""

import math
from collections import Counter
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    c = Counter(cell for row in board for cell in row)

    return X if c[X] <= c[O] else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] is EMPTY)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp_board = copy.deepcopy(board) # independent copy to avoid modifying the original board

    i, j = action
    if not (0 <= i < len(board) and 0 <= j < len(board[0])):
        raise Exception("Action out of bounds")

    if temp_board[i][j] is not EMPTY: 
        raise Exception("Action not valid. Cell is not empty.")

    temp_board[i][j] = player(board)

    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    total_size = len(board)

    for row in board:
        if row.count(row[0]) == total_size and row[0] is not EMPTY:
            return row[0]

    for j in range(total_size): 
        full_col = [board[i][j] for i in range(total_size)]
        if full_col.count(full_col[0]) == total_size and full_col[0] is not EMPTY:
            return full_col[0]

    diag_1 = [board[i][i] for i in range(total_size)]
    if diag_1.count(diag_1[0]) == total_size and diag_1[0] is not EMPTY: 
        return diag_1[0]

    diag2 = [board[i][total_size - 1 - i] for i in range(total_size)]
    if diag2.count(diag2[0]) == total_size and diag2[0] is not EMPTY:
        return diag2[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return all(cell is not EMPTY for row in board for cell in row) or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    return 1 if win == X else -1 if win == O else 0


def min_value(board, alpha, beta):
    value = math.inf
    if terminal(board): 
        return utility(board)

    for a in actions(board): 
        value = min(value, max_value(result(board, a), alpha, beta))
        beta = min(beta, value)

        if alpha >= beta: break

    return value


def max_value(board, alpha, beta):
    value = -math.inf
    if terminal(board): 
        return utility(board)

    for a in actions(board): 
        value = max(value, min_value(result(board, a), alpha, beta))
        alpha = max(alpha, value)

        if alpha >= beta: break

    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board. Applying Alpha-Beta prunning.
    """
    if terminal(board): 
        return None
    
    actual_player = player(board)
    best_move = None 

    if actual_player == X: 
        best_score = -math.inf
        # alpha and beta are shared values to compare during entire process to decide which branches we should cut
        alpha = -math.inf
        beta = math.inf

        for a in actions(board):     
            score = min_value(result(board, a), alpha, beta) # picks action that produces the highest value of min_value()
            if score > best_score: 
                best_score = score
                best_move = a

            alpha = max(alpha, best_score)
    else: 
        best_score = math.inf
        alpha = -math.inf
        beta = math.inf

        for a in actions(board):
            score = max_value(result(board, a), alpha, beta) # picks action that produces the lowest value of max_value()
            if score < best_score: 
                best_score = score
                best_move = a

            beta = min(beta, best_score)
    return best_move

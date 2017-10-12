import sys
import copy
import time
from sys import maxsize
P_Infinity = maxsize
N_Infinity = -1 * maxsize
#input_file = sys.argv[1]
out = open("output.txt", "w+")

class Board:
    def __init__(self, board, player, xs=0, os=0):
        self.board = board
        self.xScore = xs
        self.oScore = os
        self.player = player
        self.is_raid = False
        self.move = ""
        self.alpha = N_Infinity
        self.beta = P_Infinity

    def get_size(self):
        return len(self.board[0])

    def print_board(self):
        b_str = ""
        for i in range(0, self.get_size()):
            for j in range(0, self.get_size()):
                b_str += self.board[i][j]
            b_str += "\n"
            #print(self.board[i])
        return b_str

    def eval(self, player):
        if player == "X":
            return self.xScore - self.oScore
        else:
            return self.oScore - self.xScore

    def stake(self, i, j, value):
        raiding = False
        if i < self.get_size() and j < self.get_size():
            if self.board[i][j] is not ".":
                raiding = True
            if self.player is "X":
                self.xScore += int(value)
                if raiding:
                    self.oScore -= int(value)
                self.board[i][j] = "X"
            else:
                self.oScore += int(value)
                if raiding:
                    self.xScore -= int(value)
                self.board[i][j] = "O"

    def update_move(self, i, j):
        self.move = chr(ord('A')+j)+str(i+1)

class Game:
    def __init__(self, size, board, player, depth, mode, values):
        self.size = size
        self.player = player
        self.maxDepth = depth
        self.mode = mode
        self.value_board = values
        self.player_board = board
        self.free_moves = 0
        self.initialize_eval()

    def initialize_eval(self):
        for i in range(0, self.player_board.get_size()):
            for j in range(0, self.player_board.get_size()):
                # player action if position is free
                if str(self.player_board.board[i][j]) is "X":
                    self.player_board.xScore += int(self.value_board[i][j])
                elif str(self.player_board.board[i][j]) is "O":
                    self.player_board.oScore += int(self.value_board[i][j])
                elif str(self.player_board.board[i][j]) is ".":
                    self.free_moves += 1

def change_player(player_board):
    if player_board.player is "X":
        player_board.player = "O"
    else:
        player_board.player = "X"

def max_player(game, board, depth):
    player_board = copy.deepcopy(board)
    max_board = player_board
    max_eval = N_Infinity
    if game.maxDepth == depth or game.free_moves == depth:
        return board.eval(game.player), board
    depth += 1
    for i in range(0, player_board.get_size()):
        for j in range(0, player_board.get_size()):
            # player action if position is free
            if player_board.board[i][j] is "X" or player_board.board[i][j] is "O":
                continue
            else:
                # do stake or raid
                temp = copy.deepcopy(player_board)
                temp.stake(i, j, game.value_board[i][j])  # perform stake move
                stake_cur = copy.deepcopy(temp)  # board after the stake move
                change_player(temp)
                stake_eval, temp = min_player(game, temp, depth)
                if stake_eval >= max_eval:
                    if stake_eval > max_eval:
                        max_eval = stake_eval
                        max_board = copy.deepcopy(stake_cur)
                        max_board.is_raid = False
                        max_board.update_move(i, j)
                    elif max_board.is_raid:
                        max_eval = stake_eval
                        max_board = copy.deepcopy(stake_cur)
                        max_board.is_raid = False
                        max_board.update_move(i, j)
                # s_eval = temp.eval(temp.player)
                temp = copy.deepcopy(player_board)
                if raid(temp, i, j, game.value_board):
                    # call min player
                    raid_cur = copy.deepcopy(temp)
                    change_player(temp)
                    raid_eval, temp = min_player(game, temp, depth)
                    if raid_eval > max_eval:
                        max_eval = raid_eval
                        max_board = copy.deepcopy(raid_cur)
                        max_board.is_raid = True
                        max_board.update_move(i, j)
    # check if terminal condition i.e, no moves possible
    return max_eval, max_board

def min_player(game, board, depth):
    player_board = copy.deepcopy(board)
    min_eval = P_Infinity
    min_board = player_board
    if game.maxDepth == depth or game.free_moves == depth:
        return board.eval(game.player), board
    depth += 1
    for i in range(0, player_board.get_size()):
        for j in range(0, player_board.get_size()):
            # player action if position is free
            if player_board.board[i][j] is "X" or player_board.board[i][j] is "O":
                continue
            else:
                # do stake or raid
                temp = copy.deepcopy(player_board)
                # do stake
                temp.stake(i, j, game.value_board[i][j])
                stake_cur = copy.deepcopy(temp)
                change_player(temp)
                stake_eval, temp = max_player(game, temp, depth)
                if stake_eval <= min_eval:
                    if stake_eval < min_eval:
                        min_eval = stake_eval
                        min_board = copy.deepcopy(stake_cur)
                        min_board.is_raid = False
                        min_board.update_move(i, j)
                    elif min_board.is_raid:
                        min_eval = stake_eval
                        min_board = copy.deepcopy(stake_cur)
                        min_board.is_raid = False
                        min_board.update_move(i, j)
                        # do raid
                temp = copy.deepcopy(player_board)
                # call max player
                if raid(temp, i, j, game.value_board):
                    raid_cur = copy.deepcopy(temp)
                    change_player(temp)
                    raid_eval, temp = max_player(game, temp, depth)
                    if raid_eval < min_eval:
                        min_eval = raid_eval
                        min_board = copy.deepcopy(raid_cur)
                        min_board.is_raid = True
                        min_board.update_move(i, j)
    # check if terminal condition i.e, no moves possible
    return min_eval, min_board

def max_player2(game, board, depth):
    player_board = copy.deepcopy(board)
    max_eval = N_Infinity
    max_board = player_board
    if game.maxDepth == depth or game.free_moves == depth:
        return board.eval(game.player), board
    depth += 1
    stake_pruned = False
    raid_pruned = False
    for i in range(0, player_board.get_size()):
        for j in range(0, player_board.get_size()):
            if stake_pruned and raid_pruned:
                return max_board.alpha, max_board
            # player action if position is free
            if player_board.board[i][j] is "X" or player_board.board[i][j] is "O":
                continue
            else:
                # do stake
                if not stake_pruned:
                    temp = copy.deepcopy(player_board)
                    temp.stake(i, j, game.value_board[i][j])  # perform stake move
                    stake_cur = copy.deepcopy(temp)  # board after the stake move
                    change_player(temp)
                    stake_eval, temp = min_player2(game, temp, depth)
                    if stake_eval > stake_cur.alpha:
                        stake_cur.alpha = stake_eval
                    if stake_eval >= max_eval:
                        if stake_eval > max_eval:
                            max_eval = stake_eval
                            max_board = copy.deepcopy(stake_cur)
                            max_board.is_raid = False
                            max_board.update_move(i, j)
                        elif max_board.is_raid:
                            max_eval = stake_eval
                            max_board = copy.deepcopy(stake_cur)
                            max_board.is_raid = False
                            max_board.update_move(i, j)
                    if stake_cur.beta <= stake_cur.alpha:
                        stake_pruned = True
                # do raid
                if not raid_pruned:
                    temp = copy.deepcopy(player_board)
                    if raid(temp, i, j, game.value_board):
                        raid_cur = copy.deepcopy(temp)
                        change_player(temp)
                        raid_eval, temp = min_player2(game, temp, depth)
                        if raid_eval > stake_cur.alpha:
                            raid_cur.alpha = raid_eval
                        if raid_eval > max_eval:
                            max_eval = raid_eval
                            max_board = copy.deepcopy(raid_cur)
                            max_board.is_raid = True
                            max_board.update_move(i, j)
                        if raid_cur.beta <= raid_cur.alpha:
                            stake_pruned = True
    # check if terminal condition i.e, no moves possible
    return max_board.alpha, max_board

def min_player2(game, board, depth):
    player_board = copy.deepcopy(board)
    min_board = player_board
    min_eval = P_Infinity
    if game.maxDepth == depth or game.free_moves == depth:
        return board.eval(game.player), board
    depth += 1
    stake_pruned = False
    raid_pruned = False
    for i in range(0, player_board.get_size()):
        for j in range(0, player_board.get_size()):
            if stake_pruned and raid_pruned:
                return min_board.beta, min_board
            # player action if position is free
            if player_board.board[i][j] is "X" or player_board.board[i][j] is "O":
                continue
            else:
                # do stake or raid
                temp = copy.deepcopy(player_board)
                # do stake
                if not stake_pruned:
                    temp.stake(i, j, game.value_board[i][j])
                    stake_cur = copy.deepcopy(temp)
                    change_player(temp)
                    stake_eval, temp = max_player2(game, temp, depth)
                    if stake_eval < stake_cur.beta:
                        stake_cur.beta = stake_eval
                    if stake_eval <= min_eval:
                        if stake_eval < min_eval:
                            min_eval = stake_eval
                            min_board = copy.deepcopy(stake_cur)
                            min_board.is_raid = False
                            min_board.update_move(i, j)
                        elif min_board.is_raid:
                            min_eval = stake_eval
                            min_board = copy.deepcopy(stake_cur)
                            min_board.is_raid = False
                            min_board.update_move(i, j)
                    if stake_cur.beta <= stake_cur.alpha:
                        stake_pruned = True
                # do raid
                if not raid_pruned:
                    temp = copy.deepcopy(player_board)
                    # call max player
                    if raid(temp, i, j, game.value_board):
                        raid_cur = copy.deepcopy(temp)
                        change_player(temp)
                        raid_eval, temp = max_player2(game, temp, depth)
                        if raid_eval < raid_cur.beta:
                            raid_cur.beta = raid_eval
                        if raid_eval < min_eval:
                            min_eval = raid_eval
                            min_board = copy.deepcopy(raid_cur)
                            min_board.is_raid = True
                            min_board.update_move(i, j)
                        if raid_cur.beta <= raid_cur.alpha:
                            raid_pruned = True
    return min_board.beta, min_board

def raid(player_board, row, col, values):
    board = player_board.board
    size = player_board.get_size()
    can_raid = False
    raided = False
    for i in range(row-1, row+2):  # check neighbours for your pawn
        for j in range(col-1, col+2):
            if size > i >= 0 and size > j >= 0 and not (i == row and j == col) and \
                    not (i == row - 1 and (j == col - 1 or j == col + 1)) and \
                    not (i == row + 1 and (j == col - 1 or j == col + 1)):
                if board[i][j] is player_board.player:
                    can_raid = True
                    break
    if can_raid:
        player_board.stake(row, col, values[row][col])
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if size > i >= 0 and size > j >= 0 and not (i == row and j == col) and \
                        not(i == row-1 and (j == col-1 or j == col + 1)) and \
                        not (i == row+1 and (j == col-1 or j == col+1)):
                    if board[i][j] is not player_board.player and board[i][j] is not ".":
                        raided = True
                        player_board.stake(i, j, values[i][j])
    return raided

def read_input():
    with open("input.txt", 'r') as f:
        size = int(f.readline().strip())
        alg = f.readline().strip()
        if alg == "MINIMAX":
            mode = 1
        elif alg == "ALPHABETA":
            mode = 2
        player = f.readline().strip()
        depth = int(f.readline().strip())
        board_values = []
        for i in range(0, size):
            row = f.readline().strip().split(" ")
            board_values.append(row)
        player_board = []
        for i in range(0, size):
            row = list(str(f.readline().strip("\n")))
            player_board.append(row)
        player_board = Board(player_board, player, 0, 0)
        #player_board.print_board()
        game = Game(size, player_board, player, depth, mode, board_values)
        return game

def main():
    game = read_input()
    if game.mode == 1:
        val, board = max_player(game, game.player_board, 0)
    if game.mode == 2:
        val, board = max_player2(game, game.player_board, 0)
    #print val
    if board.is_raid:
        action = " Raid"
    else:
        action = " Stake"
    #print action
    #print board.move
    out.write(board.move + action+"\n")
    out.write(board.print_board())
    out.close()

#start_time = time.time()
main()
#print("--- %s seconds ---" % (time.time() - start_time))
import numpy as np
from copy import deepcopy


class Board:
    def __init__(self, board_size, starting_player):
        self.board_size = board_size
        self.board = []
        self.player = starting_player
        self.reset_board(self.player)

    def reset_board(self, starting_player):
        self.board = np.array(
            [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        )
        self.player = starting_player

    def get_state(self):
        output = ""
        for i in self.board:
            for n in i:
                if n == 1:
                    output += "1"
                elif n ==2:
                    output += "2"
                else:
                    output +="0"
                output += " "
        return output

    def get_legal_moves(self):
        flat_board = self.flatten_board()
        return [(i // self.board_size, i % self.board_size) for i in range(len(flat_board)) if flat_board[i] == 0]

    def check_legal_move(self, move):
        try:
            return self.board[move[0]][move[1]] == 0
        except IndexError:
            return False

    def make_move(self, move, player=None):
        if player:
            curplayer = player
        else: 
            curplayer = self.player
        if not self.check_legal_move(move):
            raise Exception(f"Illegal move provided: {move} {self.flatten_board()}")
        if curplayer != 1 and curplayer != 2:
            raise Exception("player must be either 1 or 2")
        self.board[move[0]][move[1]] = curplayer
        self.player = curplayer % 2 + 1

    def flatten_board(self):
        return self.board.flatten()

    def check_winning_state_player_one(self):
        reachable_nodes = []
        for i in range(self.board_size):
            if self.board[0][i] == 1:
                reachable_nodes.append((0, i))
        for node in reachable_nodes:
            for n in range(-1, 1):
                if (
                    0 <= node[1] + n < self.board_size
                    and self.board[node[0] + 1][node[1] + n] == 1
                ):
                    if node[0] + 1 == self.board_size - 1:
                        return True
                    if (
                        node[0] + 1,
                        node[1] + n,
                    ) not in reachable_nodes:  # Check if node is already added to avoid checking the same nodes twice
                        reachable_nodes.append((node[0] + 1, node[1] + n))
            if (0 <= node[1] - 1 < self.board_size
                # Check node to the left in case this has not been picked up by earlier search
                and self.board[node[0]][node[1] - 1] == 1):
                if (node[0],
                    node[1] - 1) not in reachable_nodes: 
                        reachable_nodes.append((node[0], node[1] - 1))
            if (0 <= node[1] + 1 < self.board_size
                # Check node to the left in case this has not been picked up by earlier search
                and self.board[node[0]][node[1] + 1] == 1):
                if (node[0],
                    node[1] + 1) not in reachable_nodes: 
                        reachable_nodes.append((node[0], node[1] + 1))
        return False

    def check_winning_state_player_two(self):
        reachable_nodes = []
        for i in range(self.board_size):
            if self.board[i][0] == 2:
                reachable_nodes.append((i, 0))
        for node in reachable_nodes:
            for n in range(-1, 1):
                if (
                    0 <= node[0] + n < self.board_size
                    and self.board[node[0] + n][node[1] + 1] == 2
                ):
                    if node[1] + 1 == self.board_size - 1:
                        return True
                    if (node[0] + n, node[1] + 1) not in reachable_nodes:
                        reachable_nodes.append((node[0] + n, node[1] + 1))
            if (0 <= node[0] - 1 < self.board_size
                # Check node to the left in case this has not been picked up by earlier search
                and self.board[node[0] - 1][node[1]] == 2):
                if (node[0] - 1,
                    node[1]) not in reachable_nodes: 
                        reachable_nodes.append((node[0] - 1, node[1]))
            if (0 <= node[0] + 1 < self.board_size
                # Check node to the right in case this has not been picked up by earlier search
                and self.board[node[0] + 1][node[1]] == 2):
                if (node[0] + 1,
                    node[1]) not in reachable_nodes: 
                        reachable_nodes.append((node[0] + 1, node[1]))
        return False

    def check_winning_state(self, player=0):
        """Since winning state must be checked after every move, this function
        takes in which player played the last move, to only check wheter they
        are in a winning state or not. This is to reduce the complexity of the
        algorithm.
        """
        if player == 1:
            return self.check_winning_state_player_one()
        elif player == 2:
            return self.check_winning_state_player_two()
        elif player == 0:
            return (
                self.check_winning_state_player_one()
                or self.check_winning_state_player_two()
                or len(self.get_legal_moves()) == 0
            )

    def get_reward(self, player):
        if (self.check_winning_state_player_one()):
            return 1
        else:
            return - 10

    def clone(self):
        return deepcopy(self)

import math
import random
from .board import Board
import numpy as np

class GameSimulator:

    def __init__(self, playing_board, board_size, starting_player, tree):
        self.board = Board(board_size, starting_player)
        self.playing_board = playing_board
        self.board_size = board_size
        self.tree = tree

    def initialize_root(self, state, player):
        player = player
        state_split = state.split()
        board_state = np.array([[int(i) for i in state_split[n*self.board_size:(n+1)*self.board_size]] for n in range(self.board_size)])
        self.board.player = player
        self.board.board = board_state

    def rollout_game(self, epsilon, sigma, board_copy):
        if random.uniform(0,1) > sigma:
            return self.tree.critic_evaluate(board_copy, board_copy.player)
        while not board_copy.check_winning_state():
            next_move = self.tree.rollout_action(board_copy, epsilon, board_copy.player)
            board_copy.make_move(next_move)
        return board_copy.get_reward(1)

    def tree_search(self, board_copy):
        sequence = self.tree.traverse(board_copy)
        if not sequence:
            return []
        return sequence

    def sim_games(self, epsilon, sigma, number_of_search_games):
        board_copy = self.board.clone()
        no_of_legal_moves = len(board_copy.get_legal_moves())
        dynamic_range = int(number_of_search_games/no_of_legal_moves)
        for i in range(max((dynamic_range, 10))):
            sequence = self.tree_search(board_copy)
            self.tree.expand_tree(board_copy)
            reward = self.rollout_game(epsilon, sigma, board_copy)
            sequence.reverse()
            for s in sequence:
                self.tree.update(s[0], s[1], reward)
            board_copy = self.board.clone()
        return self.tree.get_distribution(self.board)

    def reset(self, player):
        self.board = Board(self.board_size, player)


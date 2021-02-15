class Parameters():

    def __init__(self):
        # ------ VARIABLES --------
        # Board and Game Variables
        self.board_type = "D"  # "T" or "D"
        self.board_size = 5
        # For board_type = "D" and board_size = 4, open_cells must be either (1,2) or (2,1)
        self.open_cells = [(1, 1)]
        self.number_of_episodes = 600
        # Rewards
        self.winning_reward = 20
        self.losing_reward_per_peg = -3
        self.discount_per_step = -0.1
        # Visualization
        self.display_episode = True  # Display final run
        self.display_delay = 1  # Number of seconds between board updates in visualization

        # Critic Variables
        self.critic_method = "NN"  # "TL" or "NN"
        # First input parameter must be equal to number of holes on board, e.g. type D size 4 = 16
        self.critic_nn_dims = (25, 25, 30, 10, 1)
        self.lr_critic = 0.001
        self.eligibility_decay_critic = 0.95
        self.discount_factor_critic = 0.95

        # Actor Variables
        self.lr_actor = 0.1
        self.eligibility_decay_actor = 0.9
        self.discount_factor_actor = 0.95
        self.epsilon = 0.9
        self.epsilon_decay = 0.96
        # -------------------------

    def scenario_size5_triangle_tl(self):
        print("TEST")
        self.lr_actor = 0.01
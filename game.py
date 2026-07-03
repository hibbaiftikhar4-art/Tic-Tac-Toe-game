class TicTacToeGame:
    WINNING_COMBINATIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   
        (0, 4, 8), (2, 4, 6)               
    ]
    def __init__(self, player_x_name="Player 1", player_o_name="Player 2"):
        self.player_x_name = player_x_name
        self.player_o_name = player_o_name
        self.board = [""] * 9
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.winner = None
        self.winning_combination = None
        self.game_over = False
    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None
        self.winning_combination = None
        self.game_over = False
    def new_game(self, player_x_name=None, player_o_name=None):
        if player_x_name:
            self.player_x_name = player_x_name
        if player_o_name:
            self.player_o_name = player_o_name
        self.reset_board()
    def reset_scores(self):
        self.scores = {"X": 0, "O": 0, "Draws": 0}
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
    def make_move(self, position):
        if not self.is_valid_move(position):
            return False
        self.board[position] = self.current_player
        if self.check_winner():
            self.winner = self.current_player
            self.scores[self.current_player] += 1
            self.game_over = True
        elif self.check_draw():
            self.winner = "Draw"
            self.scores["Draws"] += 1
            self.game_over = True
        else:
            self.switch_player()
        return True
    def is_valid_move(self, position):
        if self.game_over:
            return False
        if not isinstance(position, int):
            return False
        if position < 0 or position > 8:
            return False
        if self.board[position] != "":
            return False
        return True
    def check_winner(self):
        for combo in self.WINNING_COMBINATIONS:
            a, b, c = combo
            if (self.board[a] == self.board[b] == self.board[c] and self.board[a] == self.current_player):
                self.winning_combination = combo
                return True
        return False
    def check_draw(self):
        return "" not in self.board
    def get_player_name(self, symbol):
        if symbol == "X":
            return self.player_x_name
        elif symbol == "O":
            return self.player_o_name
        return ""
    def get_current_player_name(self):
        return self.get_player_name(self.current_player)
import numpy as np

# Tic-Tac-Toe!

# Write a tic tac toe game. We have provided a large part of the Game class below which represents the game board during play.
# It has methods for adding a place to the board (ie. putting down an X or a O in a square) and for checking that the board
# is valid. These need to be implemented by you to pass the tests given to you. Watch out for bugs!


class Game:
    EX = 1
    OH = 2
    PLAYERS = (EX, OH)

    def __init__(self, randomize=False):
        if randomize:
            while True:
                self.board = np.random.randint(0, 3, size=(3, 3), dtype=int)
                if self.is_valid_board():
                    break
        else:
            self.board = np.zeros((3, 3), dtype=int)

    @staticmethod
    def parse_position(r, c):
        possible = 0, 1, 2
        if r not in possible or c not in possible:
            raise ValueError('Row and column must be in [0, 2]')

    def get_position(self, r, c):
        self.parse_position(r, c)
        return self.board[r, c]

    def place(self, r, c, player):
        """Place the player's marker, where `player` is EX or OH, at row `r` and column `c`."""
        # your code here
        if player not in (self.EX, self.OH):
            raise ValueError('Player must be one of (1, 2)')
        self.parse_position(r, c)
        if self.get_position(r, c):
            raise ValueError(f'Position ({r}, {c}) is already taken by player {player}')
        self.board[r, c] = player

    def check_num_plays(self):
        exes = self.board == self.EX
        ohs = self.board == self.OH
        num_exes = exes.sum()
        num_ohs = ohs.sum()
        valid_num_plays = abs(num_exes - num_ohs) <= 1
        return valid_num_plays

    def check_num_wins(self):
        exes = self.board == self.EX
        ohs = self.board == self.OH
        exes_wins = self.get_wins(exes)
        ohs_wins = self.get_wins(ohs)
        valid_num_wins = exes_wins + ohs_wins <= 1
        return valid_num_wins

    def is_valid_board(self):
        """
        Return True if this is a valid game board, it has to check for all the configurations that a valid game would
        be in. Eg. since X and O alternate during play the number of each token on the board has to reflect that.
        """
        # your code here
        return self.check_num_plays() and self.check_num_wins()

    @staticmethod
    def get_wins(player_board):
        vertical = (player_board.sum(axis=0) == 3).sum()
        horizontal = (player_board.sum(axis=1) == 3).sum()
        diag = np.all(np.diag(player_board))
        diag2 = np.all(np.diag(np.fliplr(player_board)))
        num_wins = vertical + horizontal + diag + diag2
        return num_wins


    def get_winning_player(self):
        """Returns the player number who has won the game, or None if no one has won."""
        # check rows and columns
        for r in range(3):
            row = self.board[r, :]
            col = self.board[:, r]

            for p in self.PLAYERS:
                if all(x == p for x in row):
                    return p

            for p in self.PLAYERS:
                if all(x == p for x in col):
                    return p

        # check diagonals
        for p in self.PLAYERS:
            if (
                all(x == p for x in (self.board[0, 0], self.board[1, 1], self.board[2, 2]))
                or
                all(x == p for x in (self.board[0, 2], self.board[1, 1], self.board[2, 0]))
                ):
                return p

    def __str__(self):
        symbols = [".", "X", "O"]

        rows = ["+-------+"]
        for c in range(3):
            row = ["|"]
            for r in range(3):
                row.append(symbols[self.board[r, c]])

            row.append("|")
            rows.append(" ".join(row))

        rows.append("+-------+")

        return "\n".join(rows)


def play_random_game():
    """
    Plays tic tac toe by placing alternating markers randomly on the board until it's full or one of the players wins.
    """
    game = Game()
    positions = list(np.ndindex(3, 3))  # all valid positions on the board
    move = 0

    np.random.shuffle(positions)  # randomly re-arrange the order of positions played

    while move < len(positions) and game.get_winning_player() is None:
        r, c = positions[move]
        game.place(r, c, game.PLAYERS[move % 2])
        move += 1

    return game


if __name__ == "__main__":
    print(play_random_game())

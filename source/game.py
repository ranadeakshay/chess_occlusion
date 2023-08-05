"""
This file will contain the class for creating, and updating the Chess Board in pygame.
Initially, we will use the starting position for all pieces. Later, we will need to add
code to parse FEN strings.
"""

invalid_fen_errmsg = "A valid FEN should have 6 parts. Please check input."

class game_state:
    def __init__(self):
        """
        The board is a list of lists. Each inner list represents a rank.
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.side_to_move = 'w'
        self.move_log = []

    def __init__(self, fen):
        """
        This constructor initialises the board state based on the fen notation passed to it.
        :param fen: The string containing the entire FEN notation.

        The FEN notation has six parts separated by space.
        1. piece representation from White's perspective.
        2. side to move - {w,b}
        3. Castling status
        4. En Passant possibility - indicates the target square
        5. Halfmoves since last capture or pawn advance. For 50-move rule. Not relevant here.
        6. Fullmove number. Starts at 1 and incremented after Black's move.
        """
        print(fen)
        fen = fen.split(" ")
        assert len(fen) == 6, invalid_fen_errmsg
        # we start with a list of 8 empty lists
        position = fen[0]
        ranks = position.split("/")
        self.board = [[] for i in range(8)]
        for rank,pieces in enumerate(ranks):
            for c in pieces:
                if c.isdigit():
                    c = int(c)
                    self.board[rank] += ["--" for i in range(c)]
                else:
                    if c.islower():
                        self.board[rank].append("b" + c.upper())
                    elif c.isupper():
                        self.board[rank].append("w" + c)

        self.side_to_move = fen[1]
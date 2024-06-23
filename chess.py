"""
chess board structure:
- 8x8 numpy array (data type: string)
"""
import numpy as np
import matplotlib.pyplot as plt


def singleton(class_):
    class class_w(class_):
        _instance = None

        def __new__(class2, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w, class2).__new__(class2)
                class_w._instance._sealed = False
            return class_w._instance

        def __init__(self, *args, **kwargs):
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True

    class_w.__name__ = class_.__name__
    return class_w


ChessPositionNotation = str


class ChessBoard:
    """
    ChessBoard (class)
    Chess board value object
    attributes:
        - 8x8 numpy array (data type: string)
            * state is notated as modified FEN notation style
            * example:
                rnbkqbnr
                pppppppp
                ........
                ........
                ........
                ........
                PPPPPPPP
                RNBQKBNR
        - history (list of hash value from the board)
    methods:
        - __str__ (return the board state)
        - __getitem__ (return the value of the board at the given position)
        - __setitem__ (set the value of the board at the given position)
    """

    def __init__(self):
        self.board = np.array([['.'] * 8 for _ in range(8)])

    def __str__(self):
        return str(self.board)

    def __getitem__(self, position: tuple):
        return self.board[position]

    def __setitem__(self, position: tuple, value: str):
        self.board[position] = value


class ChessBoards:
    @staticmethod
    def empty() -> ChessBoard:
        return ChessBoard()

    @staticmethod
    def initialized() -> ChessBoard:
        board = ChessBoard()
        board.board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        board.board[1] = ['p'] * 8
        board.board[6] = ['P'] * 8
        board.board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        return board

    @staticmethod
    def only_kings() -> ChessBoard:
        board = ChessBoard()
        board.board[0][4] = 'k'
        board.board[7][4] = 'K'
        return board


class ChessGame:
    """
    ChessGame (class)
    Chess game object
    attributes:
        - ChessBoard instance
        - PieceRuleManager instance
        - SpecialRuleManager instance
    note:
        - action is notated as modified Algebric Notation style
    """

    def __init__(self):
        self.board = ChessBoard()
        self.piece_rule_manager = PieceRuleManager()
        self.special_rule_manager = SpecialRuleManager()
        self.state_rule_manager = StateRuleManager()
        self.parser = AlgebraicNotationParser()

    def move(self, position1: tuple, position2: tuple):
        piece = self.board[position1]
        if piece == '.':
            return False

        self.board[position1] = '.'
        self.board[position2] = piece

        return True

    def action(self, notation: str):
        pass


@singleton
class AlgebraicNotationParser:
    def __init__(self):
        self.pieces = set('RrNnBbQqKk')
        self.files = set('abcdefgh')
        self.ranks = set('12345678')

    def position_notation_to_index(self, notation: ChessPositionNotation) -> tuple:
        return (int(notation[1]) - 1, ord(notation[0]) - ord('a'))

    def parse(self, notation: str) -> tuple:
        # castling
        if notation == 'O-O':
            return 'K', ()


@singleton
class BaseRule:
    def out_of_board(self, position: tuple) -> bool:
        return position[0] < 0 or position[0] >= 8 or position[1] < 0 or position[1] >= 8

    def is_same_position(self, position1: tuple, position2: tuple) -> bool:
        return position1 == position2

    def is_same_team(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        if board[position1].isupper() and board[position2].isupper():
            return True
        if board[position1].islower() and board[position2].islower():
            return True
        return False

    def is_blocked(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        # TODO
        # IDEA: dx, dy를 정하고, position1에서 position2까지 dx, dy만큼 증가하면서 중간에 막힌게 있는지 확인 (ex: dr = 0 dc = -1)
        # pos2가 기물의 이동가능 위치에 있고,out of board가 아니라는 전제하에 --> 누구의 책임?
        if position1[0] > position2[0]:
            dr = -1
        if position1[0] == position2[0]:
            dr = 0
        if position1[0] < position2[0]:
            dr = 1
        if position1[1] > position2[1]:
            dc = -1
        if position1[1] == position2[1]:
            dc = 0
        if position1[1] < position2[1]:
            dc = 1

        temp_position = position1
        while temp_position != position2:
            temp_position[0] += dr
            temp_position[1] += dc
            if board[temp_position] != '.':
                return True
        return False


class StateRuleManager(BaseRule):
    def __init__(self):
        self.rules: dict[str, StateRule] = {
            'check': CheckRule(),
            'checkmate': CheckmateRule(),
            'stalemate': StalemateRule(),
            'repetition': RepetitionRule(),
        }

    def check_state(self, type, board: ChessBoard, **kwargs):
        return False


class StateRule(BaseRule):
    def check_state(self, board: ChessBoard):
        raise NotImplementedError


class CheckRule(StateRule):
    def check_state(self, board: ChessBoard):
        # TODO
        return True


class CheckmateRule(StateRule):
    def check_state(self, board: ChessBoard):
        # TODO
        return True


class StalemateRule(StateRule):
    def check_state(self, board: ChessBoard):
        # TODO
        return True


class RepetitionRule(StateRule):
    def check_state(self, board: ChessBoard):
        # TODO
        return True


class MoveLimitRule(StateRule):
    def check_state(self, board: ChessBoard):
        # TODO
        return True


class SpecialRuleManager:
    def __init__(self):
        self.rules: dict[str, SpecialRule] = {'promotion': PromotionRule()}

    def validate_move(self, type, board: ChessBoard, **kwargs):
        return self.rules[type].validate_move(board, **kwargs)


class SpecialRule(BaseRule):
    def validate_move(self, **kwargs):
        raise NotImplementedError


class PromotionRule(SpecialRule):
    def validate_move(self, position: tuple, board: ChessBoard, promotion_piece: str):
        # TODO
        return True


class PieceRuleManager:
    def __init__(self):
        self.rules: dict[str, PieceRule] = {
            'P': PawnRule(),
            'R': RookRule(),
            'N': KnightRule(),
            'B': BishopRule(),
            'Q': QueenRule(),
            'K': KingRule(),
        }

    def validate_move(self, piece, position1, position2, board):
        piece_rule = self.rules.get(piece)

        if piece_rule is None:
            raise ValueError(f'Invalid piece: {piece}')

        return piece_rule.validate_move(position1, position2, board)


class PieceRule(BaseRule):
    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        raise NotImplementedError()


class PawnRule(PieceRule):
    def _is_default_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        return False

    def _is_attack_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        return False

    def _is_en_passant(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        return False

    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        if self._is_default_move(position1, position2, board):
            return True
        if self._is_attack_move(position1, position2, board):
            return True
        if self._is_en_passant(position1, position2, board):
            return True
        return False


class RookRule(PieceRule):
    def _is_default_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        if self.out_of_board(position2):
            return False
        
        if self.is_same_position(position1, position2):
            return False

        if self.is_same_team(position1, position2):
            return False

        if position1[0] != position2[0] and position1[1] != position2[1]:
            return False

        if self.is_blocked(position1, position2, board):
            return False

        return position1[0] == position2[0] or position1[1] == position2[1]

    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:

        if self._is_default_move(position1, position2, board):
            return True

        return False


class KnightRule(PieceRule):
    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        # TODO
        return True


class BishopRule(PieceRule):
    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        """
        if self.out_of_board():
            return False
        
        if self.is_same_position():
            return False
        
        if self.is_same_team():
            return False
        if 
        """
        return True


class QueenRule(PieceRule):
    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        # TODO
        return True


class KingRule(PieceRule):
    def _is_default_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        return False

    def _is_castling(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        return False

    def validate_move(self, position1: tuple, position2: tuple, board: ChessBoard) -> bool:
        """
        - 8 direction move is allowed (cannot move more than 1 step, or cannot move to the same position)
        - cannot move to the same team's piece
        - cannot move out of the board
        - castling is allowed
        """
        # TBD
        return True

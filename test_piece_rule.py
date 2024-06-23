from chess import PieceRuleManager, ChessBoards

# def test_pawn():
#     prm = PieceRuleManager()
#     assert(prm.validate_move('P', (3, 3), (3, 4)))
#     assert(prm.validate_move('P', (3, 3), (3, 5)))
#     assert(not prm.validate_move('P', (3, 3), (4, 4)))


def test_rook():
    prm = PieceRuleManager()

    board = ChessBoards.empty()
    board[3, 3] = 'R'
    print(board)

    # position이 범위를 벗어나면 false를 반환해야 한다.
    assert not prm.validate_move('R', (3, 3), (9, 9), board)

    # 같은 위치로 이동하면 false를 반환해야 한다.
    assert not prm.validate_move('R', (3, 3), (3, 3), board)

    # 같은 팀의 말이 있는 위치로 이동하면 false를 반환해야 한다.
    board = ChessBoards.initialized()
    print(board)
    assert not prm.validate_move('R', (1, 1), (3, 4), board)

    # 유효한 이동은 true를 반환해야 한다.
    board[1, 0] = '.'
    print(board)
    assert prm.validate_move('R', (0, 0), (3, 0), board)

if __name__ == '__main__':
    test_rook()

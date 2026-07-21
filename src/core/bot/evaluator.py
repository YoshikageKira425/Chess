from src.pieces.piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.king import King
from src.core.board import Board
from src.color_enum import Color

MATERIAL_SCORE = {Pawn: 1, Knight: 3, Rook:5, Bishop: 3, Queen: 9}

PAWN_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [.5, .5, .5, .5, .5, .5, .5, .5],
    [.2, .2, .2, .4, .4, .2, .2, .2],
    [.05, .05, .2, .25, .25, .2, .05, .05],
    [ 0,  0,  0, .2, .2,  0,  0,  0],
    [.05, -.05,-.2,  0,  0,-.2, -.05, .05],
    [.05, .2, .2,-.2,-.2, .2, .2, .05],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
]

KNIGHT_TABLE = [
    [-.5,-.4,-.4,-.4,-.4,-.4,-.4,-.5],
    [-.4,-.2,  0,  0,  0,  0,-.2,-.4],
    [-.4,  0, .2, .15, .15, .2,  0,-.4],
    [-.4, .05, .15, .2, .2, .15, .05,-.4],
    [-.4,  0, .15, .2, .2, .15,  0,-.4],
    [-.4, .05, .2, .15, .15, .2, .05,-.4],
    [-.4,-.2,  0, .05, .05,  0,-.2,-.4],
    [-.5,-.4,-.4,-.4,-.4,-.4,-.4,-.5],
]

BISHOP_TABLE = [
    [-.2,-.2,-.2,-.2,-.2,-.2,-.2,-.2],
    [-.2,  0,  0,  0,  0,  0,  0,-.2],
    [-.2,  0, .05, .2, .2, .05,  0,-.2],
    [-.2, .05, .05, .2, .2, .05, .05,-.2],
    [-.2,  0, .2, .2, .2, .2,  0,-.2],
    [-.2, .2, .2, .2, .2, .2, .2,-.2],
    [-.2, .05,  0,  0,  0,  0, .05,-.2],
    [-.2,-.2,-.2,-.2,-.2,-.2,-.2,-.2],
]

ROOK_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [.05, .2, .2, .2, .2, .2, .2, .05],
    [-.05,  0,  0,  0,  0,  0,  0, -.05],
    [-.05,  0,  0,  0,  0,  0,  0, -.05],
    [-.05,  0,  0,  0,  0,  0,  0, -.05],
    [-.05,  0,  0,  0,  0,  0,  0, -.05],
    [-.05,  0,  0,  0,  0,  0,  0, -.05],
    [ 0,  0,  0, .05, .05,  0,  0,  0],
]

QUEEN_TABLE = [
    [-.2,-.2,-.2, -5, -5,-.2,-.2,-.2],
    [-.2,  0,  0,  0,  0,  0,  0,-.2],
    [-.2,  0, .05, .05, .05, .05,  0,-.2],
    [ -5,  0, .05, .05, .05, .05,  0, -5],
    [  0,  0, .05, .05, .05, .05,  0, -5],
    [-.2, .05, .05, .05, .05, .05,  0,-.2],
    [-.2,  0, .05,  0,  0,  0,  0,-.2],
    [-.2,-.2,-.2, -5, -5,-.2,-.2,-.2],
]

PIECE_SQUARE_TABLES = {
    Pawn:   PAWN_TABLE,
    Knight: KNIGHT_TABLE,
    Bishop: BISHOP_TABLE,
    Rook:   ROOK_TABLE,
    Queen:  QUEEN_TABLE,
}

def evaluate(board: Board) -> int:
    if board.is_king_threatened(False):
        return 9999
    if board.is_king_threatened(True):
        return -9999
    
    score = evaluate_state(board)

    return round(score, 3)

def evaluate_state(board: Board) -> int:
    score = 0

    for row in range(8):
        for col in range(8):
            piece = board.get(row, col)

            if piece is None or isinstance(piece, King):
                continue

            material = MATERIAL_SCORE.get(type(piece), 0)
            table = PIECE_SQUARE_TABLES.get(type(piece))
            
            bonus = table[row][col] if piece.color == Color.WHITE else table[7 - row][col]

            value = material + bonus
            score += value if piece.color == Color.WHITE else -value
          
    return score

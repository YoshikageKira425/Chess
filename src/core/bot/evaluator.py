from src.pieces.piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.king import King

scores = {Pawn: 100, Knight: 320, Rook: 500, Bishop: 330, Bishop: 330, Queen: 900}

def evaluate(board: list[list[Piece]]) -> tuple:
    white_score, black_score = evaluate_pieces(board)

    return (white_score, black_score)

def evaluate_pieces(board: list[list[Piece]]) -> tuple:
    white_score = 0
    black_score = 0

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece is None or isinstance(piece, King):
                continue

            value = scores.get(type(piece), 0)

            if piece.color == "w":
                white_score += value
            else:
                black_score -= value
                
    return (white_score, black_score)
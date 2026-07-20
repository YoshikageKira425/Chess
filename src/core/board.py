from src.pieces.piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.king import King
from src.action import Action
from src.color_enum import Color


class Board:
    def __init__(self):
        self.setup_board()
        
    def setup_board(self):
        self.grid: list[list[Piece]] = [
            [Rook("bR"), Knight("bN"), Bishop("bB"), Queen("bQ"), King("bK"), Bishop("bB"), Knight("bN"), Rook("bR")],
            [Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP")],
            [Rook("wR"), Knight("wN"), Bishop("wB"), Queen("wQ"), King("wK"), Bishop("wB"), Knight("wN"), Rook("wR")],
        ]
        
        self.white_king = self.grid[7][4]
        self.black_king = self.grid[0][4]
        
        self.actions: list[Action] = []

    def get(self, row: int, col: int) -> Piece | None:
        return self.grid[row][col]

    def move(self, from_pos: tuple, to_pos: tuple) -> Piece | None:
        """Moves a piece and returns the captured piece if any."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.grid[from_row][from_col]
        piece.set_position(to_row, to_col)
        
        captured = self.grid[to_row][to_col]
        
        en_passant_captured = None
        if isinstance(piece, Pawn) and captured is None and from_col != to_col:
            en_passant_captured = self.grid[from_row][to_col]
            self.grid[from_row][to_col] = None
            captured = en_passant_captured
        
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        
        self.actions.append(Action(
            from_pos=from_pos,
            to_pos=to_pos,
            piece=piece,
            captured=captured
        ))

        return captured

    def is_valid_move(self, from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        piece = self.grid[from_row][from_col]

        if not piece:
            return False
        
        last = self.last_action()

        return piece.valid_move(self.grid, from_pos, to_pos, last)
    
    def is_promotion(self) -> bool:
        last = self.last_action()
        if last is None:
            return False

        piece = last.piece
        return isinstance(piece, Pawn) and (
            (piece.color == Color.WHITE and piece.row == 0) or
            (piece.color == Color.BLACK and piece.row == 7)
        )

    def promote(self, piece_type: str):
        """Replace the pawn with the chosen piece. Call after is_promotion()."""
        last = self.last_action()
        row, col = last.to_pos
        color = last.piece.color

        classes = {"Q": Queen, "R": Rook, "B": Bishop, "N": Knight}
        new_piece = classes[piece_type](f"{color}{piece_type}")
        new_piece.set_indexes(row, col)

        self.grid[row][col] = new_piece
        
        last.original_piece = last.piece
        last.piece = new_piece
        
    def get_legal_moves(self, color: str) -> list[tuple]:
        legal = []

        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is None or piece.color != color:
                    continue

                for to_row in range(8):
                    for to_col in range(8):
                        if not self.is_valid_move((row, col), (to_row, to_col)):
                            continue

                        self.move((row, col), (to_row, to_col))
                        in_check = self.is_king_threatened(color == Color.WHITE)
                        self.undo()

                        if not in_check:
                            legal.append(((row, col), (to_row, to_col)))

        return legal
    
    def undo(self) -> Action | None:
        if not self.actions:
            return None
        
        action = self.actions.pop()
        from_row, from_col = action.from_pos
        to_row, to_col = action.to_pos

        if action.original_piece:
            pawn = action.original_piece
            self.grid[from_row][from_col] = pawn
            pawn.set_position(from_row, from_col)
        else:
            self.grid[from_row][from_col] = action.piece
            action.piece.set_position(from_row, from_col)

        self.grid[to_row][to_col] = action.captured
        
        if action.captured is not None:
            action.captured.set_position(action.captured.row, action.captured.col)
        
        return action

    def is_king_threatened(self, turn: bool) -> bool:
        enemy_color = Color.BLACK if turn else Color.WHITE
        king = self.white_king if turn else self.black_king
        
        for row in range(8):
            for col in range(8):
                piece = self.get(row, col)
                
                if piece is None:
                    continue
                
                if enemy_color == piece.color and piece.valid_move(self.grid, (row, col), king.get_postion()):
                    return True
        
        return False
    
    def is_stalemate(self, turn: bool) -> bool:
        color = Color.WHITE if turn else Color.BLACK
        
        return not self.is_king_threatened(turn) and len(self.get_legal_moves(color)) == 0
    
    def is_checkmate(self, turn: bool) -> bool:
        color = Color.WHITE if turn else Color.BLACK
        
        return len(self.get_legal_moves(color)) == 0

    def is_within_bounds(self, row: int, col: int) -> bool:
        return 0 <= row <= 7 and 0 <= col <= 7
    
    def last_action(self) -> Action | None:
        return self.actions[-1] if self.actions else None
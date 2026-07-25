from .piece import Piece
from ..constants import HIGHLIGHT_MOVE, HIGHLIGHT_CAPTURE
from ..enum.color_enum import Color
from ..action import Action

class Pawn(Piece):
    def __init__(self, piece):
        super().__init__(piece)

    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple, last_action:Action=None) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if self.color == Color.WHITE else 1

        if (
            to_col == from_col
            and to_row == from_row + direction
            and board[to_row][to_col] is None
        ):
            return True

        if (
            self._has_pawn_moved()
            and to_col == from_col
            and to_row == from_row + direction * 2
            and board[from_row + direction][from_col] is None
            and board[to_row][to_col] is None
        ):
            return True

        if (
            abs(to_col - from_col) == 1
            and to_row == from_row + direction
        ):
            target = board[to_row][to_col]
            if target is not None and target.color != self.color:
                return True

            if self._is_en_passant(from_pos, to_pos, last_action):
                return True

        return False

    def _is_en_passant(self, from_pos:tuple, to_pos:tuple, last_action:Action) -> bool:
        if last_action is None:
            return False

        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if self.color == Color.WHITE else 1

        last_piece = last_action.piece
        last_from = last_action.from_pos
        last_to = last_action.to_pos

        if not isinstance(last_piece, Pawn):
            return False

        if abs(last_from[0] - last_to[0]) != 2:
            return False

        if last_to != (from_row, to_col):
            return False

        if to_row != from_row + direction:
            return False

        return True

    def move_highlight(self, board: list[list[Piece]], from_pos: tuple, last_action=None) -> list[tuple]:
        from_row, from_col = from_pos
        highlights = []
        direction = -1 if self.color == Color.WHITE else 1

        row = from_row + direction

        if self._capture_highlight_condition(board, row, from_col - 1):
            highlights.append((row, from_col - 1, HIGHLIGHT_CAPTURE))

        if self._capture_highlight_condition(board, row, from_col + 1):
            highlights.append((row, from_col + 1, HIGHLIGHT_CAPTURE))

        for dc in [-1, 1]:
            if self._is_en_passant(from_pos, (row, from_col + dc), last_action):
                highlights.append((row, from_col + dc, HIGHLIGHT_CAPTURE))

        if board[from_row + direction][from_col] is None:
            highlights.append((from_row + direction, from_col, HIGHLIGHT_MOVE))
        else:
            return highlights

        if self._has_pawn_moved() and board[from_row + direction * 2][from_col] is None:
            highlights.append((from_row + direction * 2, from_col, HIGHLIGHT_MOVE))

        return highlights

    def _capture_highlight_condition(self, board, row, col):
        return (
            0 <= row < 8
            and 0 <= col < 8
            and board[row][col] is not None
            and board[row][col].color != self.color
        )

    def _has_pawn_moved(self) -> bool:
        return (self.row == 6 and self.color == Color.WHITE) or (self.row == 1 and self.color == Color.BLACK)
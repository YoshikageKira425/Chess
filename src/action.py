from dataclasses import dataclass, field
from src.pieces.piece import Piece


@dataclass
class Action:
    from_pos: tuple
    to_pos: tuple
    piece: Piece
    captured: Piece | None = None
    original_piece: Piece | None = None
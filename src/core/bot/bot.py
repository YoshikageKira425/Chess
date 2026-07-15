from src.core.board import Board
import copy
from .evaluator import evaluate
from src.color_enum import Color

class Bot:
    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)
        self.max_depth = 2

    def search(self, depth: int) -> tuple:
        if depth == self.max_depth:
            return (evaluate(self.board), None, None)

        current_turn = Color.BLACK if depth % 2 == 0 else Color.WHITE
        is_minimizing = current_turn == Color.BLACK

        best_score = float('inf') if is_minimizing else float('-inf')
        best_from, best_to = None, None

        for move in self.board.get_legal_moves(current_turn):
            from_pos, to_pos = move[0], move[1]

            self.board.move(from_pos, to_pos)
            score, _, _ = self.search(depth + 1)
            self.board.undo()

            if is_minimizing and score < best_score:
                best_score, best_from, best_to = score, from_pos, to_pos
            elif not is_minimizing and score > best_score:
                best_score, best_from, best_to = score, from_pos, to_pos

        return (best_score, best_from, best_to)

        
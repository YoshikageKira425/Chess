from src.core.board import Board
from .evaluator import evaluate
from src.color_enum import Color

DIFFICULTY = {
    "easy":   1,
    "medium": 2,
    "hard":   3,
}

class Bot:
    def __init__(self, board: Board, color:Color, difficulty: str = "easy"):
        self.board = board
        self.max_depth = DIFFICULTY[difficulty]
        self.bot_color = color

    def _search_move(self, depth: int=0, alpha: float = float('-inf'), beta: float = float('inf')) -> tuple:
        if depth == self.max_depth:
            return (evaluate(self.board), None, None)

        opponent_color = Color.WHITE if self.bot_color == Color.BLACK else Color.BLACK
        current_turn = self.bot_color if depth % 2 == 0 else opponent_color
        is_minimizing = current_turn == self.bot_color

        best_score = float('inf') if is_minimizing else float('-inf')
        best_from, best_to = None, None

        for move in self.board.get_legal_moves(current_turn):
            from_pos, to_pos = move[0], move[1]

            self.board.move(from_pos, to_pos)
            score, _, _ = self._search_move(depth + 1, alpha, beta)
            self.board.undo()

            if is_minimizing and score < best_score:
                best_score, best_from, best_to = score, from_pos, to_pos
                beta = min(beta, best_score)
            elif not is_minimizing and score > best_score:
                best_score, best_from, best_to = score, from_pos, to_pos
                alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return (best_score, best_from, best_to)
    
    def chose_promotion(self) -> str:
        best_score = float('-inf')
        result = "Q"  
        alpha = float('-inf')
        beta = float('inf')
        
        for promotion in ["Q", "N", "R", "B"]:
            self.board.promote(promotion)
            
            score, _, _ = self._search_move(alpha=alpha, beta=beta)
            
            self.board.undo()
            
            if score > best_score:
                result = promotion
                best_score = score
                alpha = max(alpha, best_score)
                
        return result

    def get_move(self):
        _, from_pos, to_pos = self._search_move()
        return (from_pos, to_pos)
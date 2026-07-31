from .local_chess import LocalChess
from src.enum.difficulty_enum import Difficulty
from src.enum.color_enum import Color
from src.core.bot import Bot

class BotChess(LocalChess):
    def __init__(self, difficulty: Difficulty):
        super().__init__()
        
        self.bot = Bot(self.board, difficulty)
        
    def finish_turn(self):
        super().finish_turn()
        
        if self.bot.bot_color == self.turn:
            self.bot_move()
            
    def promotion(self):
        if self.bot.bot_color == self.turn:
            self.board.promote(self.bot.chose_promotion())
        else:
            super().promotion()
            
    def undo(self):
        super().undo()
        super().undo()
        
    def bot_move(self):
        from_pos, to_pos = self.bot.get_move()
        
        if from_pos and to_pos:
            self._move_piece(from_pos, to_pos)
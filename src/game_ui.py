import arcade
import arcade.gui

class GameUI:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True
        
        self.white_turn_texture = arcade.load_texture("assets/sprites/white_pieces/pawn_white.png")
        self.black_turn_texture = arcade.load_texture("assets/sprites/black_pieces/pawn_black.png")
        
        self.turn_indicator = arcade.gui.UIImage(
            texture=self.white_turn_texture,
            x=20,
            y=500,
            width=54,
            height=72
        )
        
        self._manager.add(self.turn_indicator)
        
    def set_turn(self, turn: bool):
        if turn:
            self.turn_indicator.texture = self.white_turn_texture
        else:
            self.turn_indicator.texture = self.black_turn_texture

    def draw(self):
        self._manager.draw()
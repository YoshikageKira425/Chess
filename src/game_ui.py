import arcade
import arcade.gui

class GameUI:
    def __init__(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager._pixelated = True
        
        self.whiteTurnTexture = arcade.load_texture("assets/sprites/white_pieces/pawn_white.png")
        self.blackTurnTexture = arcade.load_texture("assets/sprites/black_pieces/pawn_black.png")
        
        self.turnIndicator = arcade.gui.UIImage(
            texture=self.whiteTurnTexture,
            x=20,
            y=500,
            width=54,
            height=72
        )
        
        self.manager.add(self.turnIndicator)
        
    def setTurn(self, turn: bool):
        if turn:
            self.turnIndicator.texture = self.whiteTurnTexture
        else:
            self.turnIndicator.texture = self.blackTurnTexture

    def draw(self):
        self.manager.draw()
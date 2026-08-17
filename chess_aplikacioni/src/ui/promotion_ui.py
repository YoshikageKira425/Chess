import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE, BG_COLOR
from chess_core.enum.pieces_enum import Pieces

class PromotionUi:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True

        self._set_up_promotion_ui()

    def _set_up_promotion_ui(self):
        self._promotion_widget = arcade.gui.UIWidget()
        self._promotion_widget.add(arcade.gui.UISpace(
            width=800, height=600, color=(*BG_COLOR, 180)
        ))
        self._promotion_widget.add(arcade.gui.UILabel(
            text="PROMOTE", font_size=50, font_name="ArcadeClassic", x=40, y=520
        ))

        self._promotion_buttons = {}
        textures = {Pieces.QUEEN: arcade.load_texture("assets/sprites/white_pieces/queen_white.png"), Pieces.ROOK: arcade.load_texture("assets/sprites/white_pieces/tower_white.png"),
                   Pieces.BISHOP: arcade.load_texture("assets/sprites/white_pieces/bishop_white.png"), Pieces.KNIGHT: arcade.load_texture("assets/sprites/white_pieces/knight_white.png")}

        started_x = 200

        for piece_type, texture in textures.items():
            btn = arcade.gui.UITextureButton(x=started_x, y=300, width=108, height=144, texture=texture)
            
            self._promotion_widget.add(btn)
            self._promotion_buttons[piece_type] = btn
            
            started_x += 120

    def show_promotion(self, callback: callable):
        for piece_type, btn in self._promotion_buttons.items():
            def on_click(event, pt=piece_type):
                callback(pt)
                self._manager.remove(self._promotion_widget)

            btn.on_click = on_click

        self._manager.add(self._promotion_widget)

    def draw(self):
        self._manager.draw()

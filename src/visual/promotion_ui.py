import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE, BG_COLOR


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
        positions = {"Q": 200, "R": 320, "B": 440, "N": 560}
        textures = {"Q": arcade.load_texture("assets/sprites/white_pieces/queen_white.png"), "R": arcade.load_texture("assets/sprites/white_pieces/tower_white.png"),
                   "B": arcade.load_texture("assets/sprites/white_pieces/bishop_white.png"), "N": arcade.load_texture("assets/sprites/white_pieces/knight_white.png")}

        for piece_type, x in positions.items():
            btn = arcade.gui.UITextureButton(x=x, y=300, width=108, height=144, texture=textures[piece_type])
            self._promotion_widget.add(btn)
            self._promotion_buttons[piece_type] = btn

    def show_promotion(self, callback: callable):
        for piece_type, btn in self._promotion_buttons.items():
            def on_click(event, pt=piece_type):
                callback(pt)
                self._manager.remove(self._promotion_widget)

            btn.on_click = on_click

        self._manager.add(self._promotion_widget)

    def draw(self):
        self._manager.draw()

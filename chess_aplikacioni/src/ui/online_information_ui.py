import arcade
from chess_core.enum.color_enum import Color


class OnlineInformationUI:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True

        self._white_texture = arcade.load_texture(
            "assets/sprites/white_pieces/pawn_white.png")
        self._black_texture = arcade.load_texture(
            "assets/sprites/black_pieces/pawn_black.png")

        self._player_color_indicator = arcade.gui.UIImage(
            texture=self._white_texture,
            x=20,
            y=100,
            width=54,
            height=72,
        )
        self._manager.add(self._player_color_indicator)

        self._manager.add(arcade.gui.UILabel(
            text="YOUR COLOR",
            font_size=16,
            font_name="BoldPixels",
            bold=True,
            text_color=arcade.color.WHITE,
            x=7,
            y=80,
        ))

    def set_color(self, color: Color):
        is_white = color == Color.WHITE
        
        self._player_color_indicator.texture = self._white_texture \
                                                if is_white else self._black_texture

    def draw(self):
        self._manager.draw()

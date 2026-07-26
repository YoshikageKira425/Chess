import arcade
import arcade.gui
from src.enum.color_enum import Color
from src.enum.pieces_enum import Pieces
from src.constants import BAR_WIDTH, BAR_X, BAR_Y, MAX_SCORE, BUTTTON_STYLE


class ChessInformationUi:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True

        self._white_turn_texture = arcade.load_texture(
            "assets/sprites/white_pieces/pawn_white.png")
        self._black_turn_texture = arcade.load_texture(
            "assets/sprites/black_pieces/pawn_black.png")

        self._turn_indicator = arcade.gui.UIImage(
            texture=self._white_turn_texture,
            x=20,
            y=500,
            width=54,
            height=72
        )
        self._manager.add(self._turn_indicator)

        self._set_up_promotion_ui()
        self._set_up_eval_bar()

        self.update_eval(0)

    def _set_up_eval_bar(self):
        self._eval_white = arcade.gui.UISpace(
            width=264, height=20,
            color=arcade.color.WHITE
        )
        self._eval_black = arcade.gui.UISpace(
            width=264, height=20,
            color=arcade.color.BLACK
        )
        self._manager.add(self._eval_black)
        self._manager.add(self._eval_white)

    def update_eval(self, score: float):
        clamped = max(-MAX_SCORE, min(MAX_SCORE, score))
        white_width = int((BAR_WIDTH / 2) + (clamped /
                          MAX_SCORE) * (BAR_WIDTH / 2 * 0.8))
        black_width = BAR_WIDTH - white_width

        self._eval_black.width = black_width
        self._eval_black.rect = self._eval_black.rect.align_left(
            BAR_X).align_bottom(BAR_Y)

        self._eval_white.width = white_width
        self._eval_white.rect = self._eval_white.rect.align_right(
            800 - BAR_X).align_bottom(BAR_Y)

    def _set_up_promotion_ui(self):
        self._promotion_widget = arcade.gui.UIWidget()
        self._promotion_widget.add(arcade.gui.UISpace(
            width=800, height=600, color=(0, 0, 0, 180)
        ))
        self._promotion_widget.add(arcade.gui.UILabel(
            text="PROMOTE", font_size=50, font_name="ArcadeClassic", x=40, y=520
        ))

        self._promotion_buttons = {}
        positions = {Pieces.QUEEN: 420, Pieces.ROOK: 360,
                     Pieces.BISHOP: 300, Pieces.KNIGHT: 240}
        names = {Pieces.QUEEN: "QUEEN", Pieces.ROOK: "ROOK",
                 Pieces.BISHOP: "BISHOP", Pieces.KNIGHT: "KNIGHT"}

        for piece_type, y in positions.items():
            btn = arcade.gui.UIFlatButton(
                text=names[piece_type], y=y, x=40, width=250, style=BUTTTON_STYLE
            )
            self._promotion_widget.add(btn)
            self._promotion_buttons[piece_type] = btn

        self._manager.add(self._promotion_widget)
        self._manager.remove(self._promotion_widget)

    def show_promotion(self, callback: callable):
        for piece_type, btn in self._promotion_buttons.items():
            def on_click(event, pt=piece_type):
                callback(pt)
                self._manager.remove(self._promotion_widget)

            btn.on_click = on_click

        self._manager.add(self._promotion_widget)

    def set_turn(self, turn: Color):
        self._turn_indicator.texture = self._white_turn_texture if turn == Color.WHITE else self._black_turn_texture

    def draw(self):
        self._manager.draw()

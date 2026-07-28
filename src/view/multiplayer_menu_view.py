import math
import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE, FADE_SPEED, FLOAT_AMP, FLOAT_FREQ


class MultiplayerMenuView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.HUNTER_GREEN)

        self._manager = arcade.gui.UIManager()
        self._manager._pixelated = True

        self._time = 0.0
        self._white_y = 0.0
        self._black_y = 0.0
        self._fade_alpha = 255.0
        self._fade_state = "in"

        self._manager.add(arcade.gui.UIImage(
            texture=arcade.load_texture(
                "assets/sprites/board/board_with_border_02.png"),
            x=140,
            y=40,
            width=528,
            height=528,
            alpha=140
        ))

        self._manager.add(arcade.gui.UILabel(
            "CHESS", font_size=80, font_name="ArcadeClassic", y=470, x=250
        ))

        white_piece = arcade.load_texture(
            "assets/sprites/white_pieces/pawn_white.png")
        black_piece = arcade.load_texture(
            "assets/sprites/black_pieces/pawn_black.png")

        self._white_pawn = arcade.gui.UIImage(
            texture=white_piece, width=108, height=144, y=450, x=130, angle=340)
        self._black_pawn = arcade.gui.UIImage(
            texture=black_piece, width=108, height=144, y=450, x=550, angle=20)
        self._manager.add(self._white_pawn)
        self._manager.add(self._black_pawn)

        self._set_up_main_ui()

    def _set_up_main_ui(self):
        casual_play_button = arcade.gui.UIFlatButton(
            text="CASUAL PLAY", x=300, y=340, width=200, style=BUTTTON_STYLE)
        competitive_play_button = arcade.gui.UIFlatButton(
            text="COMPETITIVE PLAY", x=100, y=270, width=550, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=200, width=200, style=BUTTTON_STYLE)

        self._manager.add(casual_play_button)
        self._manager.add(competitive_play_button)
        self._manager.add(back_button)

        @casual_play_button.event("on_click")
        def casual_match(*args):
            print("Casual Match")

        @competitive_play_button.event("on_click")
        def competitive_match(*args):
            print("Competitive Match")

        @back_button.event("on_click")
        def on_back(*args):
            self.back()

    def back(self):
        from .main_menu_view import MainMenuView
        self.window.show_view(MainMenuView())

    def on_update(self, delta_time: float):
        self._time += delta_time

        new_white = math.sin(self._time * FLOAT_FREQ) * FLOAT_AMP
        new_black = math.sin(self._time * FLOAT_FREQ + math.pi) * FLOAT_AMP
        self._white_pawn.move(0, new_white - self._white_y)
        self._black_pawn.move(0, new_black - self._black_y)
        self._white_y = new_white
        self._black_y = new_black

        if self._fade_state == "in":
            self._fade_alpha = max(
                0.0, self._fade_alpha - FADE_SPEED * delta_time)
            if self._fade_alpha == 0.0:
                self._fade_state = "idle"

    def on_show_view(self):
        self._manager.enable()
        self._white_y = 0.0
        self._black_y = 0.0
        self._fade_alpha = 255.0
        self._fade_state = "in"

    def on_hide_view(self):
        self._manager.disable()

    def on_draw(self):
        self.clear()
        self._manager.draw()

        if self._fade_alpha > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(400, 300, 800, 600),
                (0, 0, 0, int(self._fade_alpha))
            )

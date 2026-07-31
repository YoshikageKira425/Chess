import math
import arcade
import arcade.gui
from ..games.local_chess import LocalChess
from ..games.bot_chess import BotChess
from .multiplayer_menu_view import MultiplayerMenuView
from src.enum.difficulty_enum import Difficulty
from src.constants import BUTTTON_STYLE, FADE_SPEED, FLOAT_AMP, FLOAT_FREQ


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.HUNTER_GREEN)

        arcade.load_font("assets/font/ARCADECLASSIC.ttf")

        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True

        self._time = 0.0
        self._white_y = 0.0
        self._black_y = 0.0
        self._fade_alpha = 255.0
        self._fade_state = "in"
        self._next_widget: arcade.gui.UIWidget | None = None

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

        white_tex = arcade.load_texture(
            "assets/sprites/white_pieces/pawn_white.png")
        black_tex = arcade.load_texture(
            "assets/sprites/black_pieces/pawn_black.png")

        self._white_pawn = arcade.gui.UIImage(
            texture=white_tex, width=108, height=144, y=450, x=130, angle=340)
        self._black_pawn = arcade.gui.UIImage(
            texture=black_tex, width=108, height=144, y=450, x=550, angle=20)
        self._manager.add(self._white_pawn)
        self._manager.add(self._black_pawn)

        self._main_widget = arcade.gui.UIWidget()
        self._difficulty_widget = arcade.gui.UIWidget()
        self._active_widget = self._main_widget

        self._set_up_main_ui()
        self._set_up_difficulty_ui()

        self._manager.add(self._main_widget)

    def _set_up_main_ui(self):
        vs_bot_button = arcade.gui.UIFlatButton(
            text="VS BOT",      x=300, y=340, width=200, height=55, style=BUTTTON_STYLE)
        vs_player_button = arcade.gui.UIFlatButton(
            text="VS PLAYER",   x=300, y=270, width=200, height=55, style=BUTTTON_STYLE)
        multiplayer_button = arcade.gui.UIFlatButton(
            text="MULTIPLAYER", x=215, y=200, width=370, height=55, style=BUTTTON_STYLE)
        quit_button = arcade.gui.UIFlatButton(
            text="QUIT",         x=300, y=130, width=200, height=55, style=BUTTTON_STYLE)

        self._main_widget.add(vs_bot_button)
        self._main_widget.add(vs_player_button)
        self._main_widget.add(multiplayer_button)
        self._main_widget.add(quit_button)

        @vs_bot_button.event("on_click")
        def on_vs_bot(*args):
            self._switch_to(self._difficulty_widget)

        @vs_player_button.event("on_click")
        def on_vs_player(*args):
            self.play(is_bot=False)

        @multiplayer_button.event("on_click")
        def on_multiplayer(*args):
            self.multiplayer()

        @quit_button.event("on_click")
        def on_quit(*args):
            self.quit()

    def _set_up_difficulty_ui(self):
        self._difficulty_widget.add(arcade.gui.UILabel(
            text="DIFFICULTY", font_size=55, font_name="ArcadeClassic", y=400, x=190
        ))

        easy_button = arcade.gui.UIFlatButton(
            text="EASY",   x=300, y=330, width=200, height=55, style=BUTTTON_STYLE)
        medium_button = arcade.gui.UIFlatButton(
            text="MEDIUM", x=300, y=260, width=200,height=55, style=BUTTTON_STYLE)
        hard_button = arcade.gui.UIFlatButton(
            text="HARD",   x=300, y=190, width=200, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK",   x=300, y=120, width=200, height=55, style=BUTTTON_STYLE)

        self._difficulty_widget.add(easy_button)
        self._difficulty_widget.add(medium_button)
        self._difficulty_widget.add(hard_button)
        self._difficulty_widget.add(back_button)

        @easy_button.event("on_click")
        def on_easy(*args):
            self.play(is_bot=True, difficulty=Difficulty.EASY)

        @medium_button.event("on_click")
        def on_medium(*args):
            self.play(is_bot=True, difficulty=Difficulty.MEDIUM)

        @hard_button.event("on_click")
        def on_hard(*args):
            self.play(is_bot=True, difficulty=Difficulty.HARD)

        @back_button.event("on_click")
        def on_back(*args):
            self._switch_to(self._main_widget)

    def _switch_to(self, widget: arcade.gui.UIWidget):
        """Begin a crossfade transition to a different sub-widget."""
        self._next_widget = widget
        self._fade_state = "out"

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
        elif self._fade_state == "out":
            self._fade_alpha = min(
                255.0, self._fade_alpha + FADE_SPEED * delta_time)
            if self._fade_alpha >= 255.0 and self._next_widget is not None:
                self._manager.remove(self._active_widget)
                self._active_widget = self._next_widget
                self._next_widget = None
                self._manager.add(self._active_widget)
                self._fade_state = "in"

    def on_show_view(self):
        self._manager.enable()
        self._white_y = 0.0
        self._black_y = 0.0
        self._fade_alpha = 255.0
        self._fade_state = "in"

    def on_hide_view(self):
        self._manager.disable()

    def play(self, is_bot: bool, difficulty: Difficulty | None = None):
        if is_bot:
            self.window.show_view(BotChess(difficulty))
        else:
            self.window.show_view(LocalChess())

    def multiplayer(self):
        self.window.show_view(MultiplayerMenuView())

    def quit(self):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self._manager.draw()

        if self._fade_alpha > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(400, 300, 800, 600),
                (0, 0, 0, int(self._fade_alpha))
            )

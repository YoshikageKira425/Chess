import math
import arcade
import arcade.gui
from ..games.local_chess import LocalChess
from ..games.bot_chess import BotChess
from .multiplayer_menu_view import MultiplayerMenuView
from chess_core.enum.difficulty_enum import Difficulty
from src.constants import BUTTTON_STYLE
from ..base.base_menu_view import BaseMenuView

class MainMenuView(BaseMenuView):
    def __init__(self):
        arcade.load_font("assets/font/ARCADECLASSIC.ttf")
        
        super().__init__()

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
            self.switch_to(self._difficulty_widget)

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
            self.switch_to(self._main_widget)

    def play(self, is_bot: bool, difficulty: Difficulty | None = None):
        if is_bot:
            self.window.show_view(BotChess(difficulty))
        else:
            self.window.show_view(LocalChess())

    def multiplayer(self):
        self.window.show_view(MultiplayerMenuView())

    def quit(self):
        arcade.exit()
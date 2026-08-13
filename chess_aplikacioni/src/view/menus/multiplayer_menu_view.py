import math
import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE, FADE_SPEED, FLOAT_AMP, FLOAT_FREQ
from ..base_menu_view import BaseMenuView
from src.core.network.account_manager import AccountManager

class MultiplayerMenuView(BaseMenuView):
    def __init__(self):
        super().__init__()

        self.account = AccountManager()

        self._set_up_main_ui()

    def _set_up_main_ui(self):
        casual_play_button = arcade.gui.UIFlatButton(
            text="CASUAL", x=300, y=340, width=200, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=270, width=200, height=55, style=BUTTTON_STYLE)

        self._manager.add(casual_play_button)
        self._manager.add(back_button)

        @casual_play_button.event("on_click")
        def play(*args):
            self.play()

        @back_button.event("on_click")
        def on_back(*args):
            self.back()

    def back(self):
        from .main_menu_view import MainMenuView
        self.window.show_view(MainMenuView())
        
    def play(self):
        player_id = self.account.get_player_id()
        if not player_id:
            return
        
        from ..games.online_chess import OnlineGameView
        self.window.show_view(OnlineGameView(player_id))

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

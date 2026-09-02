import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE
from ..base.base_menu_view import BaseMenuView
from src.core.network.account_manager import account_manager
from src.ui.leaderboard_ui import LeaderboardUI
from src.core.network.leaderboard import Leaderboard
from chess_core.enum.game_type import GameType


class MultiplayerMenuView(BaseMenuView):
    def __init__(self):
        super().__init__()

        self._leaderboard_ui = LeaderboardUI()
        self._leaderboard_widget = self._leaderboard_ui.get_widget()

        self._main_widget = arcade.gui.UIWidget()

        self._set_up_main_ui()

        self._active_widget = self._main_widget
        self._manager.add(self._active_widget)

    def _set_up_main_ui(self):
        casual_play_button = arcade.gui.UIFlatButton(
            text="CASUAL PLAY", x=220, y=340, width=370, height=55, style=BUTTTON_STYLE)
        ranked_play_button = arcade.gui.UIFlatButton(
            text="RANKED PLAY", x=220, y=270, width=370, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=130, width=200, height=55, style=BUTTTON_STYLE)

        account_label = account_manager.username or "ACCOUNT"
        self._account_button = arcade.gui.UIFlatButton(
            text=account_label, x=50, y=30, width=250, height=55, style=BUTTTON_STYLE)

        self._main_widget.add(casual_play_button)
        self._main_widget.add(ranked_play_button)
        self._main_widget.add(back_button)
        self._main_widget.add(self._account_button)

        leaderboard_button = arcade.gui.UIFlatButton(
            text="LEADERBOARD", x=220, y=200, width=370, height=55, style=BUTTTON_STYLE)
        self._main_widget.add(leaderboard_button)

        back_button_leaderboard = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=10, width=200, height=55, style=BUTTTON_STYLE)
        self._leaderboard_widget.add(back_button_leaderboard)

        @casual_play_button.event("on_click")
        def play(*args):
            self.play(GameType.CASUAL)

        @ranked_play_button.event("on_click")
        def play(*args):
            self.play(GameType.RANKED)

        @back_button.event("on_click")
        def on_back(*args):
            self.back()

        @self._account_button.event("on_click")
        def on_account(*args):
            self.account()

        @leaderboard_button.event("on_click")
        def on_leaderboard(*args):
            self.switch_to(self._leaderboard_widget)
            self._leaderboard_ui.set_data(Leaderboard.gettin_top_ten())

        @back_button_leaderboard.event("on_click")
        def on_back(*args):
            self.switch_to(self._main_widget)

    def play(self, type: GameType):
        player_id = account_manager.get_player_id()
        if not player_id:
            return

        from ..games.online_chess import OnlineGameView
        self.window.show_view(OnlineGameView(player_id, type))

    def account(self):
        from .auth_menu_view import AuthMenuView
        self.window.show_view(AuthMenuView())

    def back(self):
        from .main_menu_view import MainMenuView
        self.window.show_view(MainMenuView())


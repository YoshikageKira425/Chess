import arcade
from ..base.base_menu_view import BaseMenuView
from src.core.network.account_manager import account_manager
from src.constants import BUTTTON_STYLE
from src.core.network.leaderboard import Leaderboard


class LeaderboardView(BaseMenuView):
    def __init__(self):
        super().__init__()

        self._main_widget = arcade.gui.UIWidget()
        self._rows: list[arcade.gui.UIWidget] = []

        self.username = account_manager.username
        self.users_elo = Leaderboard.get_user_elo(
            account_manager.get_player_id())

        self._set_up_ui()
        self._set_data(Leaderboard.gettin_top_ten())

        self._active_widget = self._main_widget
        self._manager.add(self._active_widget)

    def _set_up_ui(self):
        self._main_widget.add(arcade.gui.UILabel(
            text="#", font_size=20, font_name="BoldPixels",
            x=155, y=470
        ))
        self._main_widget.add(arcade.gui.UILabel(
            text="PLAYER", font_size=20, font_name="BoldPixels",
            x=210, y=470
        ))
        self._main_widget.add(arcade.gui.UILabel(
            text="ELO", font_size=20, font_name="BoldPixels",
            x=530, y=470
        ))

        if self.username:
            self._main_widget.add(arcade.gui.UILabel(
                text=f"{self.username} elo: {self.users_elo}", font_size=20, font_name="BoldPixels",
                x=30, y=30
            ))

        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=10,
            width=200, height=55,
            style=BUTTTON_STYLE
        )
        self._main_widget.add(back_button)

        self._main_widget.add(arcade.gui.UISpace(
            x=150, y=458, width=510, height=2,
            color=(180, 180, 180, 200)
        ))

        self._rows_container = arcade.gui.UIWidget()
        self._main_widget.add(self._rows_container)

        @back_button.event("on_click")
        def on_back(*args):
            self.back()

    def _add_row(self, rank: int, username: str, elo: str, index: int):
        y = 430 - (index * 38)

        row_bg_color = (40, 43, 63, 180) if index % 2 == 0 else (
            30, 33, 50, 180)

        if username == account_manager.username:
            row_bg_color = (66, 72, 107, 180)

        self._rows_container.add(arcade.gui.UISpace(
            x=150, y=y - 6, width=510, height=36,
            color=row_bg_color
        ))

        rank_colors = {
            1: (255, 215, 0, 255),
            2: (192, 192, 192, 255),
            3: (205, 127, 50, 255),
        }
        rank_color = rank_colors.get(rank, (200, 200, 200, 255))

        self._rows_container.add(arcade.gui.UILabel(
            text=str(rank),
            font_size=18,
            font_name="BoldPixels",
            x=155, y=y,
            text_color=rank_color
        ))
        self._rows_container.add(arcade.gui.UILabel(
            text=str(username),
            font_size=18,
            font_name="BoldPixels",
            x=210, y=y,
            text_color=arcade.color.WHITE
        ))
        self._rows_container.add(arcade.gui.UILabel(
            text=str(elo),
            font_size=18,
            font_name="BoldPixels",
            x=530, y=y,
            text_color=rank_color
        ))

    def _set_data(self, players: list[dict]):
        if not players:
            return

        self._rows_container.clear()
        for i, player in enumerate(players[:10]):
            self._add_row(i + 1, player["username"],
                          str(int(player["elo"])), i)

    def back(self):
        from .multiplayer_menu_view import MultiplayerMenuView
        self.window.show_view(MultiplayerMenuView())

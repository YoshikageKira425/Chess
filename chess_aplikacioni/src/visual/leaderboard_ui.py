import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE


class LeaderboardUI(arcade.gui.UIWidget):
    def __init__(self):
        super().__init__()

        self._widget = arcade.gui.UIWidget()
        self._rows: list[arcade.gui.UIWidget] = []

        self._set_up_ui()

    def _set_up_ui(self):
        self._widget.add(arcade.gui.UILabel(
            text="#", font_size=20, font_name="ArcadeClassic",
            x=155, y=470
        ))
        self._widget.add(arcade.gui.UILabel(
            text="PLAYER", font_size=20, font_name="ArcadeClassic",
            x=210, y=470
        ))
        self._widget.add(arcade.gui.UILabel(
            text="ELO", font_size=20, font_name="ArcadeClassic",
            x=530, y=470
        ))

        self._widget.add(arcade.gui.UISpace(
            x=150, y=458, width=510, height=2,
            color=(180, 180, 180, 200)
        ))

        self._rows_container = arcade.gui.UIWidget()
        self._widget.add(self._rows_container)

    def _add_row(self, rank: int, username: str, elo: str, index: int):
        y = 430 - (index * 38)

        row_bg_color = (40, 43, 63, 180) if index % 2 == 0 else (30, 33, 50, 180)

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
            font_name="ArcadeClassic",
            x=155, y=y,
            text_color=rank_color
        ))
        self._rows_container.add(arcade.gui.UILabel(
            text=str(username),
            font_size=18,
            font_name="ArcadeClassic",
            x=210, y=y,
            text_color=arcade.color.WHITE
        ))
        self._rows_container.add(arcade.gui.UILabel(
            text=str(elo),
            font_size=18,
            font_name="ArcadeClassic",
            x=530, y=y,
            text_color=rank_color
        ))

    def set_data(self, players: list[dict]):
        if not players:
            return
        
        self._rows_container.clear()
        for i, player in enumerate(players[:10]):
            self._add_row(i + 1, player["username"], str(int(player["elo"])), i)

    def get_widget(self) -> arcade.gui.UIWidget:
        return self._widget
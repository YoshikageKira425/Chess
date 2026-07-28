import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE
from src.enum.color_enum import Color

_FADE_SPEED = 400   # alpha units per second


class EndScreenUi:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager._pixelated = True
        self._manager.disable()
        self._show = False
        self._enter_alpha = 255.0   # starts fully black, fades to 0

        self._white_king_texture = arcade.load_texture("assets/sprites/white_pieces/king_white.png")
        self._black_king_texture = arcade.load_texture("assets/sprites/black_pieces/king_black.png")

        self._set_up_ui()

    def _set_up_ui(self):
        self._manager.add(arcade.gui.UISpace(width=800, height=600, color=(135, 135, 135, 150)))

        self._label = arcade.gui.UILabel(
            text="WHITE WINS",
            font_size=55,
            font_name="ArcadeClassic",
            y=480,
            x=40
        )
        self._manager.add(self._label)

        self._piece_image = arcade.gui.UIImage(
            texture=self._white_king_texture,
            x=40,
            y=290,
            width=120,
            height=160
        )
        self._manager.add(self._piece_image)

        self._restart_button = arcade.gui.UIFlatButton(
            text="RESTART",
            y=190,
            x=40,
            width=250,
            style=BUTTTON_STYLE
        )
        self._manager.add(self._restart_button)

        self._main_menu_button = arcade.gui.UIFlatButton(
            text="MAIN MENU",
            y=120,
            x=40,
            width=285,
            style=BUTTTON_STYLE
        )
        self._manager.add(self._main_menu_button)

    def set_up_ui_buttons(self, restart_func: callable, main_menu_func: callable):
        self._restart_button.on_click   = lambda _: restart_func()
        self._main_menu_button.on_click = lambda _: main_menu_func()

    def show_end_screen(self, winner: Color | None = None):
        self._manager.enable()
        self._show        = True
        self._enter_alpha = 255.0   # reset fade each time

        if winner:
            tex   = self._white_king_texture if winner == Color.WHITE else self._black_king_texture
            label = "WHITE WINS" if winner == Color.WHITE else "BLACK WINS"
        else:
            tex   = self._white_king_texture
            label = "STALEMATE"

        self._piece_image.texture = tex
        self._label.label.text    = label  # update the underlying pyglet label

    def hide_end_screen(self):
        self._manager.disable()
        self._show = False

    def update(self, delta_time: float):
        if not self._show:
            return
        if self._enter_alpha > 0:
            self._enter_alpha = max(0.0, self._enter_alpha - _FADE_SPEED * delta_time)

    def draw(self):
        if not self._show:
            return
        self._manager.draw()
        if self._enter_alpha > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(400, 300, 800, 600),
                (0, 0, 0, int(self._enter_alpha))
            )

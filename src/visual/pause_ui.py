import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE

_FADE_SPEED = 400


class PauseUi:
    def __init__(self):
        self._pause_manager = arcade.gui.UIManager()
        self._pause_manager.disable()
        self._is_paused   = False
        self._enter_alpha = 255.0   # starts fully black, fades to 0 on show

        self._set_up_pause_ui()

    def _set_up_pause_ui(self):
        self._pause_manager.add(arcade.gui.UISpace(width=800, height=600, color=(135, 135, 135, 150)))

        self._pause_manager.add(arcade.gui.UILabel(text="PAUSED", font_size=60, font_name="ArcadeClassic", y=520, x=40))

        self._resume_button     = arcade.gui.UIFlatButton(text="RESUME",    y=420, x=40, width=225, style=BUTTTON_STYLE)
        self._restart_button    = arcade.gui.UIFlatButton(text="RESTART",   y=360, x=40, width=250, style=BUTTTON_STYLE)
        self._main_menu_button  = arcade.gui.UIFlatButton(text="MAIN MENU", y=300, x=40, width=285, style=BUTTTON_STYLE)

        self._pause_manager.add(self._resume_button)
        self._pause_manager.add(self._restart_button)
        self._pause_manager.add(self._main_menu_button)

    def set_up_ui_buttons(self, resume_func: callable, restart_func: callable, main_menu_func: callable):
        self._resume_button.on_click    = lambda _: resume_func()
        self._restart_button.on_click   = lambda _: restart_func()
        self._main_menu_button.on_click = lambda _: main_menu_func()

    def pause(self, value: bool):
        self._is_paused = value
        if value:
            self._enter_alpha = 255.0   # reset fade each time pause opens
            self._pause_manager.enable()
        else:
            self._pause_manager.disable()

    def update(self, delta_time: float):
        if not self._is_paused:
            return
        if self._enter_alpha > 0:
            self._enter_alpha = max(0.0, self._enter_alpha - _FADE_SPEED * delta_time)

    def draw(self):
        if not self._is_paused:
            return
        self._pause_manager.draw()
        if self._enter_alpha > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(400, 300, 800, 600),
                (0, 0, 0, int(self._enter_alpha))
            )

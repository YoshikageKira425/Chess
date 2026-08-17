import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE, FADE_SPEED, GOLD, BG_COLOR


class PauseUi:
    def __init__(self):
        self._pause_manager = arcade.gui.UIManager()
        self._pause_manager.disable()
        self._is_paused = False
        self._alpha = 0.0
        self._target = 0.0

        self._set_up_pause_ui()
        self._snapshot_button_styles()

    def _set_up_pause_ui(self):
        self._background = arcade.gui.UISpace(
            width=800, height=600, color=(*BG_COLOR, 0)
        )
        self._pause_manager.add(self._background)

        self._label = arcade.gui.UILabel(
            text="PAUSED", font_size=60, text_color=GOLD, font_name="ArcadeClassic", y=500, x=40
        )
        self._pause_manager.add(self._label)

        self._resume_button = arcade.gui.UIFlatButton(
            text="RESUME",    y=420, x=40, width=225, height=55, style=BUTTTON_STYLE)
        self._restart_button = arcade.gui.UIFlatButton(
            text="RESTART",   y=350, x=40, width=250, height=55, style=BUTTTON_STYLE)
        self._main_menu_button = arcade.gui.UIFlatButton(
            text="MAIN MENU", y=280, x=40, width=285, height=55, style=BUTTTON_STYLE)

        self._pause_manager.add(self._resume_button)
        self._pause_manager.add(self._restart_button)
        self._pause_manager.add(self._main_menu_button)

    def _snapshot_button_styles(self):
        """Capture each button's original RGB values once so animation never drifts."""
        self._buttons = (self._resume_button,
                         self._restart_button, self._main_menu_button)
        self._btn_base = []
        for btn in self._buttons:
            base = {}
            for state, style in btn.style.items():
                base[state] = {
                    "fc": tuple(style.font_color[:3]),
                    "bg": tuple(style.bg[:3]),
                }
            self._btn_base.append(base)

    def set_up_ui_buttons(self, resume_func: callable, restart_func: callable, main_menu_func: callable):
        self._resume_button.on_click = lambda _: resume_func()
        self._restart_button.on_click = lambda _: restart_func()
        self._main_menu_button.on_click = lambda _: main_menu_func()

    def remove_restart_button(self):
        self._pause_manager.remove(self._restart_button)

    def pause(self, value: bool):
        if value:
            self._is_paused = True
            self._target = 255.0
            self._pause_manager.enable()
        else:
            self._target = 0.0
            self._pause_manager.disable()

    def update(self, delta_time: float):
        if not self._is_paused:
            return

        step = FADE_SPEED * delta_time
        if self._alpha < self._target:
            self._alpha = min(self._alpha + step, 255.0)
        elif self._alpha > self._target:
            self._alpha = max(self._alpha - step, 0.0)
            if self._alpha <= 0.0:
                self._is_paused = False

        self._apply_alpha()

    def _apply_alpha(self):
        a = int(self._alpha)

        self._background.color = (*BG_COLOR, int(self._alpha * 150 / 255))

        self._label.update_font(font_color=(*GOLD, a))

        for btn, base in zip(self._buttons, self._btn_base):
            for state, style in btn.style.items():
                r, g, b = base[state]["fc"]
                style.font_color = (r, g, b, a)
                r, g, b = base[state]["bg"]
                style.bg = (r, g, b, a)
            btn.trigger_full_render()

    def draw(self):
        if not self._is_paused:
            return
        self._pause_manager.draw()

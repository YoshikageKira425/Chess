import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE, FADE_SPEED, GOLD, BG_COLOR
from chess_core.enum.color_enum import Color


class EndScreenUi:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager._pixelated = True
        self._manager.disable()
        self._show = False
        self._alpha = 0.0  
        self._target = 0.0

        self._white_king_texture = arcade.load_texture(
            "assets/sprites/white_pieces/king_white.png")
        self._black_king_texture = arcade.load_texture(
            "assets/sprites/black_pieces/king_black.png")

        self._set_up_ui()
        self._snapshot_button_styles()

    def _set_up_ui(self):
        self._background = arcade.gui.UISpace(
            width=800, height=600, color=(*BG_COLOR, 0)
        )
        self._manager.add(self._background)

        self._label = arcade.gui.UILabel(
            text="WHITE WINS", font_size=55, font_name="BoldPixels", y=480, x=40
        )
        self._manager.add(self._label)

        self._piece_image = arcade.gui.UIImage(
            texture=self._white_king_texture, x=40, y=320, width=120, height=160
        )
        self._manager.add(self._piece_image)

        self._restart_button = arcade.gui.UIFlatButton(
            text="REPLAY", y=250, x=40, width=250, height=55, style=BUTTTON_STYLE
        )
        self._manager.add(self._restart_button)

        self._main_menu_button = arcade.gui.UIFlatButton(
            text="MAIN MENU", y=180, x=40, width=285, height=55, style=BUTTTON_STYLE
        )
        self._manager.add(self._main_menu_button)

    def _snapshot_button_styles(self):
        self._buttons = (self._restart_button, self._main_menu_button)
        self._btn_base = []
        for btn in self._buttons:
            base = {}
            for state, style in btn.style.items():
                base[state] = {
                    "fc": tuple(style.font_color[:3]),
                    "bg": tuple(style.bg[:3]),
                }
            self._btn_base.append(base)

    def set_up_ui_buttons(self, restart_func: callable, main_menu_func: callable):
        self._restart_button.on_click = lambda _: restart_func()
        self._main_menu_button.on_click = lambda _: main_menu_func()

    def show_end_screen(self, winner: Color | None = None, custom_label: str | None = None):
        self._manager.enable()
        self._show = True
        self._target = 255.0

        if winner:
            tex = self._white_king_texture if winner == Color.WHITE else self._black_king_texture
            label = "WHITE WINS" if winner == Color.WHITE else "BLACK WINS"
        else:
            tex = self._white_king_texture
            label = "STALEMATE"
            
        if custom_label:
            label = custom_label

        self._piece_image.texture = tex
        self._label.text = label

    def hide_end_screen(self):
        self._target = 0.0
        self._manager.disable() 

    def update(self, delta_time: float):
        if not self._show:
            return

        step = FADE_SPEED * delta_time
        if self._alpha < self._target:
            self._alpha = min(self._alpha + step, 255.0)
        elif self._alpha > self._target:
            self._alpha = max(self._alpha - step, 0.0)
            if self._alpha <= 0.0:
                self._show = False

        self._apply_alpha()

    def _apply_alpha(self):
        a = int(self._alpha)

        self._background.color = (*BG_COLOR, int(self._alpha * 150 / 255))
        self._piece_image.alpha = a

        self._label.update_font(font_color=(*GOLD, a))

        for btn, base in zip(self._buttons, self._btn_base):
            for state, style in btn.style.items():
                r, g, b = base[state]["fc"]
                style.font_color = (r, g, b, a)
                r, g, b = base[state]["bg"]
                style.bg = (r, g, b, a)
            btn.trigger_full_render()

    def draw(self):
        if not self._show:
            return
        self._manager.draw()

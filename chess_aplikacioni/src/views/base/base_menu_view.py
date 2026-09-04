import math
import arcade
import arcade.gui
from src.constants import FADE_SPEED, FLOAT_AMP, FLOAT_FREQ


class BaseMenuView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.HUNTER_GREEN)
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
            "CHESS", font_size=80, font_name="BoldPixels", y=470, x=250
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

    def switch_to(self, widget: arcade.gui.UIWidget):
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

    def on_draw(self):
        self.clear()
        self._manager.draw()

        if self._fade_alpha > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(400, 300, 800, 600),
                (0, 0, 0, int(self._fade_alpha))
            )

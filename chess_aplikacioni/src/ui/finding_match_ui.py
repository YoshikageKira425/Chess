import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE

class FindingMatchUI:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()

        self._manager.add(
            arcade.gui.UILabel(
                "Finding Match!!",
                font_size=60,
                font_name="BoldPixels",
                y=270, x=130
            )
        )

        self._exit_button = arcade.gui.UIFlatButton(
            text="EXIT", x=50, y=50, width=140, height=55, style=BUTTTON_STYLE)
        
        self._manager.add(self._exit_button)

    def set_up_exit_button(self, exit_func: callable):
        self._exit_button.on_click = lambda _: exit_func()

    def disable(self):
        self._manager.disable()

    def draw(self):
        self._manager.draw()

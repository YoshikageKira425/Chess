import arcade
import arcade.gui


class FindingMatchUI:
    def __init__(self):
        self._manager = arcade.gui.UIManager()

        self._manager.add(
            arcade.gui.UILabel(
                "Finding Match!!",
                font_size=60,
                font_name="BoldPixels",
                y=270, x=100
            )
        )
        
    def draw(self):
        self._manager.draw()

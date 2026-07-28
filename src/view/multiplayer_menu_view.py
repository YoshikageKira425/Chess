import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE

class MultiplayerMenuView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GREEN)

        self._manager = arcade.gui.UIManager()
        self._manager._pixelated = True

        white_piece = arcade.load_texture(
            "assets/sprites/white_pieces/pawn_white.png")
        black_piece = arcade.load_texture(
            "assets/sprites/black_pieces/pawn_black.png")

        self._manager.add(arcade.gui.UILabel(
            "CHESS", font_size=80, font_name="ArcadeClassic", y=470, x=250
        ))
        self._manager.add(arcade.gui.UIImage(
            texture=white_piece, width=108, height=144, y=450, x=130, angle=340))
        self._manager.add(arcade.gui.UIImage(
            texture=black_piece, width=108, height=144, y=450, x=550, angle=20))
        
        self._set_up_main_ui()

    def _set_up_main_ui(self):
        casual_play_button = arcade.gui.UIFlatButton(
            text="CASUAL PLAY", x=300, y=340, width=200, style=BUTTTON_STYLE)
        competitive_play_button = arcade.gui.UIFlatButton(
            text="COMPETITIVE PLAY", x=100, y=270, width=550, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=200, width=200, style=BUTTTON_STYLE)

        self._manager.add(casual_play_button)
        self._manager.add(competitive_play_button)
        self._manager.add(back_button)

        @casual_play_button.event("on_click")
        def casual_match(*args):
            print("Casual Match")

        @competitive_play_button.event("on_click")
        def competitive_match(*args):
            print("Competitive Match")

        @back_button.event("on_click")
        def on_back(*args):
            self.back()
            
    def back(self):
        from .main_menu_view import MainMenuView
        
        self.window.show_view(MainMenuView)

    def on_hide_view(self):
        self._manager.disable()

    def on_show_view(self):
        self._manager.enable()
        
    def on_draw(self):
        self.clear()
        
        self._manager.draw()

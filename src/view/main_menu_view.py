import arcade
import arcade.gui
from .game_view import GameView

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY)

        arcade.load_font("assets/font/ARCADECLASSIC.ttf")

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager._pixelated = True

        style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=45,
                font_color=arcade.color.WHITE,
                bg=(120, 120, 120),
                font_name="ArcadeClassic",
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=45,
                font_color=arcade.color.WHITE,
                bg=(90, 90, 90),
                font_name="ArcadeClassic"
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=45,
                font_color=arcade.color.WHITE,
                bg=(60, 60, 60),
                font_name="ArcadeClassic"
            ),
        }

        white_piece = arcade.load_texture("assets/sprites/white_pieces/pawn_white.png")
        black_piece = arcade.load_texture("assets/sprites/black_pieces/pawn_black.png")

        self.manager.add(arcade.gui.UILabel(
            "CHESS",
            font_size=80,
            font_name="ArcadeClassic",
            y=470,
            x=250
        ))
        self.manager.add(arcade.gui.UIImage(texture=white_piece, width=108, height=144, y=450, x=130, angle=340))
        self.manager.add(arcade.gui.UIImage(texture=black_piece, width=108, height=144, y=450, x=550, angle=20))

        play_button = arcade.gui.UIFlatButton(text="PLAY", x=300, y=340, width=200, style=style)
        quit_button = arcade.gui.UIFlatButton(text="QUIT", x=300, y=270, width=200, style=style)

        self.manager.add(play_button)
        self.manager.add(quit_button)

        @play_button.event("on_click")
        def on_play(*args):
            self.play()

        @quit_button.event("on_click")
        def on_quit(*args):
            self.quit()

    def play(self):
        game_view = GameView()
        self.window.show_view(game_view)

    def quit(self):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()
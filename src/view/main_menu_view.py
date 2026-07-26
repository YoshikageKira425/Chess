import arcade
import arcade.gui
from .base_chess_view import BaseChess

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY)

        arcade.load_font("assets/font/ARCADECLASSIC.ttf")

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager._pixelated = True

        self.style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=45, font_color=arcade.color.WHITE,
                bg=(120, 120, 120), font_name="ArcadeClassic",
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=45, font_color=arcade.color.WHITE,
                bg=(90, 90, 90), font_name="ArcadeClassic"
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=45, font_color=arcade.color.WHITE,
                bg=(60, 60, 60), font_name="ArcadeClassic"
            ),
        }

        white_piece = arcade.load_texture("assets/sprites/white_pieces/pawn_white.png")
        black_piece = arcade.load_texture("assets/sprites/black_pieces/pawn_black.png")

        self.manager.add(arcade.gui.UILabel(
            "CHESS", font_size=80, font_name="ArcadeClassic", y=470, x=250
        ))
        self.manager.add(arcade.gui.UIImage(texture=white_piece, width=108, height=144, y=450, x=130, angle=340))
        self.manager.add(arcade.gui.UIImage(texture=black_piece, width=108, height=144, y=450, x=550, angle=20))

        self._main_widget = arcade.gui.UIWidget()
        self._difficulty_widget = arcade.gui.UIWidget()

        self._set_up_main_ui()
        self._set_up_difficulty_ui()

        self.manager.add(self._main_widget)

    def _set_up_main_ui(self):
        vs_bot_button  = arcade.gui.UIFlatButton(text="VS BOT",    x=300, y=340, width=200, style=self.style)
        vs_player_button = arcade.gui.UIFlatButton(text="VS PLAYER", x=300, y=270, width=200, style=self.style)
        quit_button    = arcade.gui.UIFlatButton(text="QUIT",      x=300, y=200, width=200, style=self.style)

        self._main_widget.add(vs_bot_button)
        self._main_widget.add(vs_player_button)
        self._main_widget.add(quit_button)

        @vs_bot_button.event("on_click")
        def on_vs_bot(*args):
            self.manager.remove(self._main_widget)
            self.manager.add(self._difficulty_widget)

        @vs_player_button.event("on_click")
        def on_vs_player(*args):
            self.play(is_bot=False, difficulty="easy")

        @quit_button.event("on_click")
        def on_quit(*args):
            self.quit()

    def _set_up_difficulty_ui(self):
        self._difficulty_widget.add(arcade.gui.UILabel(
            text="DIFFICULTY", font_size=55, font_name="ArcadeClassic", y=400, x=190
        ))

        easy_button   = arcade.gui.UIFlatButton(text="EASY",   x=300, y=330, width=200, style=self.style)
        medium_button = arcade.gui.UIFlatButton(text="MEDIUM",  x=300, y=260, width=200, style=self.style)
        hard_button   = arcade.gui.UIFlatButton(text="HARD",   x=300, y=190, width=200, style=self.style)
        back_button   = arcade.gui.UIFlatButton(text="BACK",   x=300, y=120, width=200, style=self.style)

        self._difficulty_widget.add(easy_button)
        self._difficulty_widget.add(medium_button)
        self._difficulty_widget.add(hard_button)
        self._difficulty_widget.add(back_button)

        @easy_button.event("on_click")
        def on_easy(*args):
            self.play(is_bot=True, difficulty="easy")

        @medium_button.event("on_click")
        def on_medium(*args):
            self.play(is_bot=True, difficulty="medium")

        @hard_button.event("on_click")
        def on_hard(*args):
            self.play(is_bot=True, difficulty="hard")

        @back_button.event("on_click")
        def on_back(*args):
            self.manager.remove(self._difficulty_widget)
            self.manager.add(self._main_widget)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()

    def play(self, is_bot: bool, difficulty: str):
        self.window.show_view(BaseChess())

    def quit(self):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()
import arcade
import arcade.gui

class GameUI:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True
        
        self.white_turn_texture = arcade.load_texture("assets/sprites/white_pieces/pawn_white.png")
        self.black_turn_texture = arcade.load_texture("assets/sprites/black_pieces/pawn_black.png")
        self.white_king_texture = arcade.load_texture("assets/sprites/white_pieces/king_white.png")
        self.black_king_texture = arcade.load_texture("assets/sprites/black_pieces/king_black.png")
        
        self._turn_indicator = arcade.gui.UIImage(
            texture=self.white_turn_texture,
            x=20,
            y=500,
            width=54,
            height=72
        )
        
        self._button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=45,
                font_color=arcade.color.WHITE,
                bg=(135, 135, 135, 63), 
                font_name="ArcadeClassic",
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=45,
                font_color=(194, 194, 194),
                bg=(135, 135, 135, 63), 
                font_name="ArcadeClassic"
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=45,
                font_color=(145, 145, 145),
                bg=(135, 135, 135, 63), 
                font_name="ArcadeClassic"
            ),
        }
        
        self._pause_widget = arcade.gui.UIWidget()
        self._win_widget = arcade.gui.UIWidget()

        self._set_up_pause_ui()
        self._set_up_win_ui()
        self._set_up_promotion_ui()
        
        self._manager.add(self._turn_indicator)
    
    def _set_up_pause_ui(self):
        self._pause_widget.add(arcade.gui.UISpace(width=800, height=600, color=(135, 135, 135, 150)))
        
        self._pause_widget.add(arcade.gui.UILabel(text="PAUSED", font_size=60, font_name="ArcadeClassic", y=520, x=40))
        
        self._resume_button = arcade.gui.UIFlatButton(text="RESUME", y=420, x=40, width=225, style=self._button_style)
        self._pause_widget.add(self._resume_button)
        
        self._restart_button = arcade.gui.UIFlatButton(text="RESTART", y=360, x=40, width=250, style=self._button_style)
        self._pause_widget.add(self._restart_button)
        
        self._main_menu_button = arcade.gui.UIFlatButton(text="MAIN MENU", y=300, x=40, width=285, style=self._button_style)
        self._pause_widget.add(self._main_menu_button)
    
    def _set_up_win_ui(self):
        self._win_widget.add(arcade.gui.UISpace(width=800, height=600, color=(135, 135, 135, 150)))

        self._win_label = arcade.gui.UILabel(
            text="WHITE WINS",
            font_size=55,
            font_name="ArcadeClassic",
            y=480,
            x=40
        )
        self._win_widget.add(self._win_label)

        self._win_piece_image = arcade.gui.UIImage(
            texture=self.white_king_texture,
            x=40,
            y=290,
            width=120,
            height=160
        )
        self._win_widget.add(self._win_piece_image)

        self._win_restart_button = arcade.gui.UIFlatButton(
            text="RESTART",
            y=190,
            x=40,
            width=250,
            style=self._button_style
        )
        self._win_widget.add(self._win_restart_button)

        self._win_main_menu_button = arcade.gui.UIFlatButton(
            text="MAIN MENU",
            y=120,
            x=40,
            width=285,
            style=self._button_style
        )
        self._win_widget.add(self._win_main_menu_button)
    
    def win(self, who_wins: bool):
        self._win_label.text = "WHITE WINS" if who_wins else "BLACK WINS"
        self._win_piece_image.texture = self.white_king_texture if who_wins else self.black_king_texture
        self._manager.add(self._win_widget)

    def remove_win(self):
        try:
            self._manager.remove(self._win_widget)
        except Exception:
            pass
    
    def set_up_ui_buttons(self, resume_func: callable, restart_func: callable):
        def on_resume(event):
            resume_func()

        def on_restart(event):
            restart_func()

        self._restart_button.on_click = on_restart
        self._resume_button.on_click = on_resume
        self._win_restart_button.on_click = on_restart
        
    def _set_up_promotion_ui(self):
        self._promotion_widget = arcade.gui.UIWidget()
        self._promotion_widget.add(arcade.gui.UISpace(
            width=800, height=600, color=(0, 0, 0, 180)
        ))
        self._promotion_widget.add(arcade.gui.UILabel(
            text="PROMOTE", font_size=50, font_name="ArcadeClassic", x=40, y=520
        ))

        self._promotion_buttons = {}
        positions = {"Q": 420, "R": 360, "B": 300, "N": 240}
        names = {"Q": "QUEEN", "R": "ROOK", "B": "BISHOP", "N": "KNIGHT"}

        for piece_type, y in positions.items():
            btn = arcade.gui.UIFlatButton(
                text=names[piece_type], y=y, x=40, width=250, style=self._button_style
            )
            self._promotion_widget.add(btn)
            self._promotion_buttons[piece_type] = btn

        self._manager.add(self._promotion_widget)  # pre-add but hide
        self._manager.remove(self._promotion_widget)

    def show_promotion(self, callback: callable):
        for piece_type, btn in self._promotion_buttons.items():
            def on_click(event, pt=piece_type):
                callback(pt)
                self._manager.remove(self._promotion_widget)

            btn.on_click = on_click

        self._manager.add(self._promotion_widget)
        
    def set_turn(self, turn: bool):
        if turn:
            self._turn_indicator.texture = self.white_turn_texture
        else:
            self._turn_indicator.texture = self.black_turn_texture
            
    def pause(self):
        self._manager.add(self._pause_widget)

    def unpause(self):
        self._manager.remove(self._pause_widget)

    def draw(self):
        self._manager.draw()
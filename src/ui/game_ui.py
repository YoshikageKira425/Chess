import arcade
import arcade.gui

class GameUI:
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True
        
        self.white_turn_texture = arcade.load_texture("assets/sprites/white_pieces/pawn_white.png")
        self.black_turn_texture = arcade.load_texture("assets/sprites/black_pieces/pawn_black.png")
        
        self._turn_indicator = arcade.gui.UIImage(
            texture=self.white_turn_texture,
            x=20,
            y=500,
            width=54,
            height=72
        )
        
        button_style = {
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
        
        self._pause_widget.add(arcade.gui.UISpace(width=800, height=600, color=(135, 135, 135, 150)))
        
        self._pause_widget.add(arcade.gui.UILabel(text="PAUSED", font_size=60, font_name="ArcadeClassic", y=520, x=40))
        
        self._resume_button = arcade.gui.UIFlatButton(text="RESUME", y=420, x=40, width=225, style=button_style)
        
        self._pause_widget.add(self._resume_button)
        
        self._restart_button = arcade.gui.UIFlatButton(text="RESTART", y=360, x=40, width=250, style=button_style)
        
        self._pause_widget.add(self._restart_button)
        
        self._pause_widget.add(arcade.gui.UIFlatButton(text="MAIN MENU", y=300, x=40, width=285, style=button_style))
        
        self._manager.add(self._turn_indicator)
        
    def set_up_ui(self, resume_func: callable, restart_func: callable):
        def on_resume(event):
            resume_func()
            
        def on_restart(event):
            restart_func()

        self._restart_button.on_click = on_restart
        self._resume_button.on_click = on_resume
        
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
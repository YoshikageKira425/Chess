import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE

class PauseUi():
    def __init__(self):
        self._pause_manager = arcade.gui.UIManager()
        self._pause_manager.disable()
        
        self._set_up_pause_ui()
                
        self._is_paused = False
    
    def _set_up_pause_ui(self):
        self._pause_manager.add(arcade.gui.UISpace(width=800, height=600, color=(135, 135, 135, 150)))
        
        self._pause_manager.add(arcade.gui.UILabel(text="PAUSED", font_size=60, font_name="ArcadeClassic", y=520, x=40))
        
        self._resume_button = arcade.gui.UIFlatButton(text="RESUME", y=420, x=40, width=225, style=BUTTTON_STYLE)
        self._pause_manager.add(self._resume_button)
        
        self._restart_button = arcade.gui.UIFlatButton(text="RESTART", y=360, x=40, width=250, style=BUTTTON_STYLE)
        self._pause_manager.add(self._restart_button)
        
        self._main_menu_button = arcade.gui.UIFlatButton(text="MAIN MENU", y=300, x=40, width=285, style=BUTTTON_STYLE)
        self._pause_manager.add(self._main_menu_button)
        
    def set_up_ui_buttons(self, resume_func: callable, restart_func: callable, main_menu_func: callable):
        def on_resume(event):
            resume_func()

        def on_restart(event):
            restart_func()
            
        def on_main_menu(event):
            main_menu_func()

        self._restart_button.on_click = on_restart
        self._resume_button.on_click = on_resume
        self._main_menu_button.on_click = on_main_menu    
    
    def pause(self, value:bool):
        self._is_paused = value
        
        if value:
            self._pause_manager.enable()
        else:
            self._pause_manager.disable()
        
    def draw(self):
        if self._is_paused:
            self._pause_manager.draw()
            
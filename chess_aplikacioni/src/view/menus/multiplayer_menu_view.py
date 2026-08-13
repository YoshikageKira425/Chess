import math
import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE
from ..base_menu_view import BaseMenuView
from src.core.network.account_manager import AccountManager

class MultiplayerMenuView(BaseMenuView):
    def __init__(self):
        super().__init__()
        
        self.account = AccountManager()
        
        self._main_widget = arcade.gui.UIWidget()
        self._account_widget = arcade.gui.UIWidget()
        
        self._active_widget = self._main_widget

        self._set_up_main_ui()
        self._set_up_account()
        
        self._manager.add(self._main_widget)

    def _set_up_main_ui(self):
        casual_play_button = arcade.gui.UIFlatButton(
            text="PLAY", x=300, y=340, width=200, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=270, width=200, height=55, style=BUTTTON_STYLE)
        account_button = arcade.gui.UIFlatButton(
            text="Account", x=50, y=30, width=250, height=55, style=BUTTTON_STYLE)

        self._main_widget.add(casual_play_button)
        self._main_widget.add(back_button)
        self._main_widget.add(account_button)

        @casual_play_button.event("on_click")
        def play(*args):
            self.play()

        @back_button.event("on_click")
        def on_back(*args):
            self.back()
            
        @account_button.event("on_click")
        def on_account(*args):
            self.switch_to(self._account_widget)
            
    def _set_up_account(self):
        signup_button = arcade.gui.UIFlatButton(
            text="SIGN UP", x=300, y=340, width=200, height=55, style=BUTTTON_STYLE)
        login_button = arcade.gui.UIFlatButton(
            text="LOG IN", x=300, y=270, width=200, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=200, width=200, height=55, style=BUTTTON_STYLE)
        
        self._account_widget.add(signup_button)
        self._account_widget.add(login_button)
        self._account_widget.add(back_button)
        
        @signup_button.event("on_click")
        def on_signup(*args):
            print("Sign up")
                    
        @login_button.event("on_click")
        def on_login(*args):
            print("Login")
            
        @back_button.event("on_click")
        def on_back(*args):
            self.switch_to(self._main_widget)     
        
    def play(self):
        player_id = self.account.get_player_id()
        if not player_id:
            return
        
        from ..games.online_chess import OnlineGameView
        self.window.show_view(OnlineGameView(player_id))

    def back(self):
        from .main_menu_view import MainMenuView
        self.window.show_view(MainMenuView())

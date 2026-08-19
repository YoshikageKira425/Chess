import arcade
import arcade.gui
from src.constants import BUTTTON_STYLE
from ..base.base_menu_view import BaseMenuView
from src.core.network.account_manager import account_manager
from src.ui.leaderboard_ui import LeaderboardUI
from src.core.network.leaderboard import Leaderboard


class MultiplayerMenuView(BaseMenuView):
    def __init__(self):
        super().__init__()

        self._form_mode = "login"

        self._leaderboard_ui = LeaderboardUI()
        self._leaderboard_widget = self._leaderboard_ui.get_widget()

        self._main_widget = arcade.gui.UIWidget()
        self._account_widget = arcade.gui.UIWidget()
        self._form_widget = arcade.gui.UIWidget()

        self._set_up_main_ui()
        self._set_up_account()
        self._set_up_form()

        self._active_widget = self._main_widget
        self._manager.add(self._active_widget)

    def _set_up_main_ui(self):
        casual_play_button = arcade.gui.UIFlatButton(
            text="PLAY", x=300, y=340, width=200, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=200, width=200, height=55, style=BUTTTON_STYLE)

        account_label = account_manager.username or "ACCOUNT"
        self._account_button = arcade.gui.UIFlatButton(
            text=account_label, x=50, y=30, width=250, height=55, style=BUTTTON_STYLE)

        self._main_widget.add(casual_play_button)
        self._main_widget.add(back_button)
        self._main_widget.add(self._account_button)

        leaderboard_button = arcade.gui.UIFlatButton(
            text="LEADERBOARD", x=220, y=270, width=370, height=55, style=BUTTTON_STYLE)
        self._main_widget.add(leaderboard_button)

        back_button_leaderboard = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=10, width=200, height=55, style=BUTTTON_STYLE)
        self._leaderboard_widget.add(back_button_leaderboard)

        @casual_play_button.event("on_click")
        def play(*args):
            self.play()

        @back_button.event("on_click")
        def on_back(*args):
            self.back()

        @self._account_button.event("on_click")
        def on_account(*args):
            self.switch_to(self._account_widget)

        @leaderboard_button.event("on_click")
        def on_leaderboard(*args):
            self.switch_to(self._leaderboard_widget)
            self._leaderboard_ui.set_data(Leaderboard.gettin_top_ten())

        @back_button_leaderboard.event("on_click")
        def on_back(*args):
            self.switch_to(self._main_widget)

    def _set_up_account(self):
        signup_button = arcade.gui.UIFlatButton(
            text="SIGN UP", x=285, y=340, width=230, height=55, style=BUTTTON_STYLE)
        login_button = arcade.gui.UIFlatButton(
            text="LOG IN", x=285, y=270, width=230, height=55, style=BUTTTON_STYLE)
        logout_button = arcade.gui.UIFlatButton(
            text="LOG OUT", x=285, y=200, width=230, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=130, width=200, height=55, style=BUTTTON_STYLE)
        
        toggle_on  = arcade.load_texture("assets/ui/toggle_on.png")
        toggle_off = arcade.load_texture("assets/ui/toggle_off.png")

        _save_me_toggle = arcade.gui.UITextureToggle(
            on_texture=toggle_on,
            off_texture=toggle_off,
            x=50, y=50,
            width=50, height=50,
            value=True
        )
        _save_me_label = arcade.gui.UILabel(
            text="REMEMBER ME",
            font_size=18,
            font_name="BoldPixels",
            x=110, y=62,
            text_color=arcade.color.WHITE
        )

        self._account_widget.add(signup_button)
        self._account_widget.add(login_button)
        self._account_widget.add(logout_button)
        self._account_widget.add(back_button)
        self._account_widget.add(_save_me_toggle)
        self._account_widget.add(_save_me_label)

        @signup_button.event("on_click")
        def on_signup(*args):
            self._form_mode = "signup"
            self._form_title.text = "SIGN UP"
            self._submit_button.text = "SIGN UP"
            self.username_input.text = ""
            self.password_input.text = ""
            self.switch_to(self._form_widget)

        @login_button.event("on_click")
        def on_login(*args):
            self._form_mode = "login"
            self._form_title.text = "LOG IN"
            self._submit_button.text = "LOG IN"
            self.username_input.text = ""
            self.password_input.text = ""
            self.switch_to(self._form_widget)

        @logout_button.event("on_click")
        def on_logout(*args):
            account_manager.logout()
            self._account_button.text = "ACCOUNT"
            self.switch_to(self._main_widget)

        @back_button.event("on_click")
        def on_back(*args):
            self.switch_to(self._main_widget)
            
        @_save_me_toggle.event("on_change")
        def on_toggle_change(event):
            self._on_save_me_changed(event.new_value)

    def _set_up_form(self):
        self._form_title = arcade.gui.UILabel(
            text="SIGN UP",
            font_size=55,
            font_name="BoldPixels",
            x=280, y=400
        )

        self._status_label = arcade.gui.UILabel(
            text="Username taken or password too short",
            font_size=26,
            font_name="BoldPixels",
            x=300, y=155,
            text_color=arcade.color.RED
        )
        self._status_label.text = ""

        self.username_input = arcade.gui.UIInputText(
            text="", x=285, y=350,
            width=230, height=40,
            font_size=20, font_name="BoldPixels"
        )
        self.password_input = arcade.gui.UIInputText(
            text="", x=285, y=280,
            width=230, height=40,
            font_size=20, font_name="BoldPixels"
        )

        self._submit_button = arcade.gui.UIFlatButton(
            text="LOG IN", x=285, y=210,
            width=230, height=55, style=BUTTTON_STYLE
        )
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=140,
            width=200, height=55, style=BUTTTON_STYLE
        )

        self._form_widget.add(self._form_title)
        self._form_widget.add(self.username_input)
        self._form_widget.add(self.password_input)
        self._form_widget.add(self._submit_button)
        self._form_widget.add(back_button)
        self._form_widget.add(self._status_label)

        @self._submit_button.event("on_click")
        def on_submit(*args):
            self._handle_submit()

        @back_button.event("on_click")
        def on_back(*args):
            self._status_label.text = ""
            self.switch_to(self._account_widget)

    def _handle_submit(self):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self._status_label.text = "Fill in all fields"
            return

        if self._form_mode == "login":
            success = account_manager.login(username, password)
            if success:
                self._account_button.text = account_manager.username
                self._status_label.text = ""
                self.switch_to(self._main_widget)
            else:
                self._status_label.text = "Invalid credentials"

        elif self._form_mode == "signup":
            success = account_manager.signup(username, password)
            if success:
                self._account_button.text = account_manager.username
                self._status_label.text = ""
                self.switch_to(self._main_widget)
            else:
                self._status_label.text = "Username taken or password too short"

    def play(self):
        player_id = account_manager.get_player_id()
        if not player_id:
            return

        from ..games.online_chess import OnlineGameView
        self.window.show_view(OnlineGameView(player_id))

    def back(self):
        from .main_menu_view import MainMenuView
        self.window.show_view(MainMenuView())

    def _on_save_me_changed(self, value: bool):
        account_manager.remeber_me = value

import arcade
import arcade.gui
from ..base.base_menu_view import BaseMenuView
from src.core.network.account_manager import account_manager
from src.constants import BUTTTON_STYLE


class AuthMenuView(BaseMenuView):
    def __init__(self):
        super().__init__()

        self._form_mode = "login"

        self._account_widget = arcade.gui.UIWidget()
        self._form_widget = arcade.gui.UIWidget()

        self._set_up_account()
        self._set_up_form()

        self._active_widget = self._account_widget
        self._manager.add(self._active_widget)

    def _set_up_account(self):
        self.signup_button = arcade.gui.UIFlatButton(
            text="SIGN UP", x=285, y=340, width=230, height=55, style=BUTTTON_STYLE)
        self.login_button = arcade.gui.UIFlatButton(
            text="LOG IN", x=285, y=270, width=230, height=55, style=BUTTTON_STYLE)
        self.logout_button = arcade.gui.UIFlatButton(
            text="LOG OUT", x=285, y=200, width=230, height=55, style=BUTTTON_STYLE)
        back_button = arcade.gui.UIFlatButton(
            text="BACK", x=300, y=130, width=200, height=55, style=BUTTTON_STYLE)

        toggle_on = arcade.load_texture("assets/ui/toggle_on.png")
        toggle_off = arcade.load_texture("assets/ui/toggle_off.png")

        _save_me_toggle = arcade.gui.UITextureToggle(
            on_texture=toggle_on,
            off_texture=toggle_off,
            x=50, y=50,
            width=50, height=50,
            value=account_manager.remeber_me
        )
        _save_me_label = arcade.gui.UILabel(
            text="REMEMBER ME",
            font_size=18,
            font_name="BoldPixels",
            x=110, y=62,
            text_color=arcade.color.WHITE
        )

        if account_manager.is_logged_in():
            self._account_widget.add(self.logout_button)
        else:
            self._account_widget.add(self.signup_button)
            self._account_widget.add(self.login_button)

        self._account_widget.add(back_button)
        self._account_widget.add(_save_me_toggle)
        self._account_widget.add(_save_me_label)

        @self.signup_button.event("on_click")
        def on_signup(*args):
            self._form_mode = "signup"
            self._form_title.text = "SIGN UP"
            self._submit_button.text = "SIGN UP"
            self.username_input.text = ""
            self.password_input.text = ""
            self.switch_to(self._form_widget)

        @self.login_button.event("on_click")
        def on_login(*args):
            self._form_mode = "login"
            self._form_title.text = "LOG IN"
            self._submit_button.text = "LOG IN"
            self.username_input.text = ""
            self.password_input.text = ""
            self.switch_to(self._form_widget)

        @self.logout_button.event("on_click")
        def on_logout(*args):
            self._logout()

        @back_button.event("on_click")
        def on_back(*args):
            self.back()

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
                self.back()
            else:
                self._status_label.text = "Invalid credentials"
        elif self._form_mode == "signup":
            success = account_manager.signup(username, password)
            if success:
                self.back()
            else:
                self._status_label.text = "Username taken or password too short"

    def _logout(self):
        account_manager.logout()
        self.back()

    def _on_save_me_changed(self, value: bool):
        account_manager.remeber_me = value

    def back(self):
        from .multiplayer_menu_view import MultiplayerMenuView
        self.window.show_view(MultiplayerMenuView())
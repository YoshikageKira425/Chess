import arcade
from src.view.menus.main_menu_view import MainMenuView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Chess"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MainMenuView())
    arcade.run()

if __name__ == "__main__":
    main()
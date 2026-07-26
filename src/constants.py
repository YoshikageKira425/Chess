import arcade.gui

SQUARE_SIZE = 60
BOARD_OFFSET_X = 194
BOARD_OFFSET_Y = 95

HIGHLIGHT_SELECTED = (255, 255, 0, 120)   # yellow, semi-transparent
HIGHLIGHT_MOVE = (0, 255, 0, 80)       # green, semi-transparent
HIGHLIGHT_CAPTURE = (255, 0, 0, 120)      # red, semi-transparent

BAR_WIDTH = 528      
BAR_X = 140         
BAR_Y = 15          
MAX_SCORE = 10.0

BUTTTON_STYLE = {
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

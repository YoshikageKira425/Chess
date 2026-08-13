import arcade.gui

SQUARE_SIZE = 60
BOARD_OFFSET_X = 194
BOARD_OFFSET_Y = 95

HIGHLIGHT_SELECTED = (255, 215, 0,  140)   # gold
HIGHLIGHT_MOVE = (49, 99, 49, 180)   # green
HIGHLIGHT_CAPTURE = (220,  60,  60, 140)  # red

SERVER_URL = "http://localhost:8000"

BAR_WIDTH = 521.5
BAR_X = 140
BAR_Y = 15
MAX_SCORE = 10.0

FADE_SPEED = 550
FLOAT_AMP = 12
FLOAT_FREQ = 1.8

BG_COLOR = (15,  15,  25)           # near-black navy
GOLD = (212, 175,  55)          # chess gold accent
GOLD_DIM = (160, 130,  35)          # muted gold for press state

BUTTTON_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_size=45,
        font_color=arcade.color.WHITE,
        bg=(35, 38, 58),
        font_name="ArcadeClassic",
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_size=45,
        font_color=GOLD,       # gold on hover
        bg=(50, 55, 80),
        font_name="ArcadeClassic",
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_size=45,
        font_color=GOLD_DIM,       # dimmed gold on press
        bg=(25, 28, 45),
        font_name="ArcadeClassic",
    ),
}

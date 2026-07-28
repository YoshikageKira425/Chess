import arcade.gui

SQUARE_SIZE = 60
BOARD_OFFSET_X = 194
BOARD_OFFSET_Y = 95

HIGHLIGHT_SELECTED = (255, 215, 0,  140)   # gold
HIGHLIGHT_MOVE = (49, 99, 49, 180)   # green
HIGHLIGHT_CAPTURE = (220,  60,  60, 140)  # red

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
PANEL_BG = (25,  28,  45, 235)      # dark panel interior
PANEL_BORDER = (212, 175,  55, 200)     # gold panel border

BUTTTON_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_size=45,
        font_color=arcade.color.WHITE,
        bg=(35, 38, 58, 190),
        font_name="ArcadeClassic",
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_size=45,
        font_color=(212, 175, 55),       # gold on hover
        bg=(50, 55, 80, 210),
        font_name="ArcadeClassic",
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_size=45,
        font_color=(160, 130, 35),       # dimmed gold on press
        bg=(25, 28, 45, 230),
        font_name="ArcadeClassic",
    ),
}

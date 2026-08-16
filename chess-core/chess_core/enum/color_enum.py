from enum import StrEnum

class Color(StrEnum):
    BLACK = "b"
    WHITE = "w"

    def inverted(self) -> "Color":
        return Color.BLACK if self is Color.WHITE else Color.WHITE
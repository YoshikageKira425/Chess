import arcade
from .game_visual import GameVisual
from .pieces.piece import Piece


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.selected = None

        self.board = [
            [Piece("bR"), Piece("bN"), Piece("bB"), Piece("bQ"), Piece("bK"), Piece("bB"), Piece("bN"), Piece("bR")],
            [Piece("bP"), Piece("bP"), Piece("bP"), Piece("bP"),Piece("bP"), Piece("bP"), Piece("bP"), Piece("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP")],
            [Piece("wR"), Piece("wN"), Piece("wB"), Piece("wQ"), Piece("wK"), Piece("wB"), Piece("wN"), Piece("wR")],
        ]
        self.setupBoard(self.board)
        
        self.visual = GameVisual(self.board)

    def setupBoard(self, board: list[list[Piece]]):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece.setButtonCallback(lambda row=row, col=col: self.onPieceClicked(row, col))
                    
    def onPieceClicked(self, row: int, col: int):
        if self.selected is None:
            self.selected = (row, col)
        else:
            self.movePiece(self.selected, (row, col))

    def movePiece(self, fromPos: tuple, toPos: tuple):
        fromRow, fromCol = fromPos
        toRow, toCol = toPos
        
        if fromRow == toRow and fromCol == toCol:
            self.selected = None
            return

        piece = self.board[fromRow][fromCol]
        
        captured = self.board[toRow][toCol]
        if captured is not None:
            self.visual.manager.remove(captured.pieceButton)

        self.board[toRow][toCol] = piece
        self.board[fromRow][fromCol] = None

        piece.setPosition(toRow, toCol)

        piece.setButtonCallback(lambda r=toRow, c=toCol: self.onPieceClicked(r, c))

        self.selected = None

    def on_mouse_press(self, x, y, button, modifiers):
        if self.selected is not None:
            col = round((x - 175 - 18) / 60)
            row = round((600 - 110 + 24 - y) / 60)

            if 0 <= row <= 7 and 0 <= col <= 7:
                to_piece = self.board[row][col]
                if to_piece is None:
                    self.movePiece(self.selected, (row, col))

    def on_draw(self):
        self.clear()
        self.visual.draw()

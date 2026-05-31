# ♟️ Chess Game

A chess game built with Python and the [Arcade](https://api.arcade.academy/) framework.

## Features

- Visual chess board with piece sprites
- Click to select and move pieces
- Piece capture on landing
- Clean separation between game logic and visuals

## Project Structure

```
chess/
├── assets/
│   ├── sound/
│   └── sprites/
├── src/
│   ├── game/
│   │   ├── pieces/        # Piece class with sprite and position logic
│   │   ├── game_ui.py     # UI components
│   │   ├── game_view.py   # Main arcade View, handles input and game state
│   │   └── game_visual.py # UIManager, renders board and pieces
│   └── util/              # Shared utilities
├── main.py                # Entry point
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.10+
- [arcade](https://api.arcade.academy/) 3.3+

## Installation

```bash
# Clone the repo
git clone https://github.com/YoshikageKira425/chess-game.git
cd chess-game

# Install dependencies
uv sync
```

## Running the Game

```bash
python main.py
```

## How to Play

- **Click a piece** to select it (your color).
- **Click a destination square** (empty or occupied) to move the selected piece there.
- Clicking an occupied square captures that piece.
- Click the same piece again to deselect it.

> Chess rules (legal move validation, check, checkmate) are not yet enforced — pieces can move to any square.

## Roadmap

- [ ] Legal move validation per piece type
- [ ] Turn enforcement (white/black alternation)
- [ ] Check and checkmate detection
- [ ] Move highlighting
- [ ] Game over screen
- [ ] Move history / notation

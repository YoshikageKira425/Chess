# Chess Game

A full-featured chess application built with Python, split into three packages: a shared game logic core, an Arcade-powered desktop client, and a FastAPI multiplayer server.

## Project Structure

```
chess/
├── chess-core/               # Shared library: rules, board, pieces
│   └── chess_core/
│       ├── pieces/           # Bishop, King, Knight, Pawn, Queen, Rook
│       ├── enum/             # Color, GameType, Difficulty, Piece enums
│       ├── board.py          # Board state and legal move generation
│       └── action.py         # Move/action representation
│
├── chess_aplikacioni/        # Desktop client (Python Arcade)
│   ├── assets/
│   │   ├── sprites/          # Piece and board sprites
│   │   ├── font/
│   │   └── ui/
│   ├── src/
│   │   ├── constants.py      # Theme colors, animation constants
│   │   ├── core/
│   │   │   ├── ai/           # Bot engine (evaluator + search)
│   │   │   ├── network/      # HTTP account manager, leaderboard, WebSocket
│   │   │   └── data_manager.py
│   │   ├── rendering/
│   │   │   └── chess_visual.py  # Board and piece rendering
│   │   ├── ui/               # In-game overlays
│   │   │   ├── chess_information_ui.py  # Turn label, eval bar, captured pieces
│   │   │   ├── end_screen_ui.py         # Win/loss/draw screen with fade
│   │   │   ├── pause_ui.py              # Pause menu with fade
│   │   │   ├── promotion_ui.py          # Pawn promotion picker
│   │   │   ├── finding_match_ui.py      # Matchmaking waiting screen
│   │   │   ├── online_information_ui.py # Opponent info during online play
│   │   │   ├── leaderboard_ui.py
│   │   │   └── pause_online_ui.py
│   │   └── views/
│   │       ├── base/
│   │       │   ├── base_chess_view.py   # Shared chess view logic
│   │       │   └── base_menu_view.py    # Animated menu base (floating pawns, fade)
│   │       ├── games/
│   │       │   ├── local_chess.py       # Local two-player
│   │       │   ├── bot_chess.py         # vs AI bot
│   │       │   └── online_chess.py      # Online multiplayer via WebSocket
│   │       └── menus/
│   │           ├── main_menu_view.py
│   │           └── multiplayer_menu_view.py
│   └── main.py
│
└── chess_server/             # Multiplayer backend (FastAPI + SQLite)
    ├── src/
    │   ├── controller/       # Auth, games, users, leaderboard
    │   ├── core/
    │   │   ├── queue.py      # Async matchmaking queue
    │   │   └── game_manager.py
    │   ├── db/
    │   │   ├── database.py
    │   │   └── models/       # User, Game, Move ORM models
    │   ├── routes/
    │   │   ├── auth.py
    │   │   ├── games.py
    │   │   ├── leaderboard.py
    │   │   └── websocket.py  # Real-time game WebSocket handler
    │   └── schema/
    └── main.py
```

## Features

### Client
- Local two-player mode
- vs AI bot with difficulty levels
- Online multiplayer (casual and ranked)
- Full chess rules: legal move validation, check, checkmate, stalemate, en passant, castling, pawn promotion
- Dark-themed UI with gold accents and animated menus (floating pawns, crossfade transitions)
- In-game overlays: pause menu, end screen, eval bar, turn indicator — all with per-element fade animations

### Server
- JWT authentication (register/login)
- Async matchmaking queue — pairs players by game type (casual/ranked)
- Real-time game via WebSocket: move validation, resignation, timeout, disconnect handling
- ELO rating updates for ranked matches
- Leaderboard endpoint
- SQLite database via SQLAlchemy (async)

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Installation

```bash
git clone https://github.com/YoshikageKira425/chess-game.git
cd chess-game

# Install the shared core library
cd chess-core && uv sync && cd ..

# Install the desktop client
cd chess_aplikacioni && uv sync && cd ..

# Install the server
cd chess_server && uv sync && cd ..
```

## Running

### Desktop client

```bash
cd chess_aplikacioni
python main.py
```

### Multiplayer server

```bash
cd chess_server
python main.py
```

## How to Play

- **Click a piece** to select it (highlights legal moves).
- **Click a highlighted square** to move there.
- Captures, castling, en passant, and promotion are handled automatically.
- **Pause** via the in-game button to resume, restart, or return to the main menu.
- In **online mode**, connect to a server, log in, then queue for casual or ranked — the game starts automatically when an opponent is found.

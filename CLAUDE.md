# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python learning/practice repository containing multiple standalone Python projects:

1. **Ship Obstacle Avoidance Game** (`src/main.py` and `game.py`) - A pygame-based space shooter where the player controls a ship avoiding asteroids and shooting them down
2. **GUI Calculator** (`gui_calculator.py`) - A tkinter-based calculator with a blue theme
3. **Test Scripts** (`test_install.py`, `helloworld.py`) - Simple test scripts for verifying Python installation

## Environment Setup

**Python Version**: 3.14.2 (via Homebrew on macOS)

**Virtual Environment**: Located in `.venv/`

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Install dependencies (primarily pygame):
```bash
pip install pygame-ce
```

## Running Projects

### Ship Obstacle Avoidance Game

Two versions exist:
- Enhanced version with lasers, explosions, high scores: `python src/main.py`
- Simpler version: `python game.py`

**Controls**:
- WASD: Move ship
- SPACE: Shoot laser (src/main.py only)
- R: Restart after game over
- ESC: Exit game (src/main.py only)

### GUI Calculator

```bash
python gui_calculator.py
```

### Test Scripts

```bash
python test_install.py  # Interactive test script
python helloworld.py    # Basic hello world
```

## Code Architecture

### Ship Obstacle Avoidance Game (`src/main.py`)

**Game Loop Structure**:
- Event handling (pygame events, keyboard input)
- Game state updates (movement, collision detection, scoring)
- Rendering (draw stars, ship, asteroids, lasers, explosions, UI)

**Key Components**:
- **Ship**: Player-controlled spaceship with WASD movement
- **Asteroids**: Randomly generated obstacles that move from right to left
- **Lasers**: Projectiles fired by the player (SPACE key) that destroy asteroids
- **Explosions**: Visual effects when asteroids are destroyed
- **Stars**: Parallax scrolling background for visual depth
- **High Score System**: Persistent storage in `high_score.txt` with player name

**Collision Detection**:
- Ship-asteroid: Circular collision detection using distance formula
- Laser-asteroid: Rectangle-based collision detection

**State Management**:
- `game_over`: Boolean flag for game state
- `name_input_active`: Controls high score name entry flow
- High score persisted to file format: `{score}:{player_name}`

### GUI Calculator (`gui_calculator.py`)

**Class Structure**:
- Single `CalculatorApp` class encapsulates all functionality
- Uses tkinter for GUI framework

**Internal State**:
- `current`: Current display value
- `previous`: Previous value for operations
- `operator`: Selected operator (+, -, ×, ÷)
- `should_reset_display`: Flag to clear display on next digit entry

**Operations**: Basic arithmetic (+, -, ×, ÷), percentage, sign toggle, clear

## File Persistence

- `high_score.txt`: Stores high score and player name in format `{score}:{player_name}`
- The game reads this file on startup and writes to it when a new high score is achieved

## Development Notes

- Both game files (`game.py` and `src/main.py`) are standalone - `src/main.py` is the more feature-rich version
- pygame uses a standard game loop pattern: event handling → update → render → clock tick
- The calculator uses immediate execution model (not RPN or expression parsing)

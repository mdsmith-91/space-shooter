# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a pygame-based space shooter game where the player controls a ship, avoiding and shooting down asteroids. The project includes automated Windows executable builds via GitHub Actions.

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

## Running the Game

```bash
python src/main.py
```

**Controls**:
- WASD or Arrow keys: Move ship
- SPACE: Shoot laser
- R: Restart after game over
- ESC: Exit game

## Code Architecture

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

## File Persistence

- `high_score.txt`: Stores high score and player name in format `{score}:{player_name}`
- The game reads this file on startup and writes to it when a new high score is achieved

## Development Notes

- pygame uses a standard game loop pattern: event handling → update → render → clock tick
- The game includes a GitHub Actions workflow for automated Windows .exe builds
- PyInstaller is used for creating standalone executables

## Building for Distribution

See `BUILD.md` for detailed instructions on creating Windows executables. The project includes:
- `.github/workflows/build-windows.yml` - Automated CI/CD builds
- `build_windows.bat` - Manual build script for Windows systems
- `DISTRIBUTE_README.txt` - End-user instructions to include with the executable

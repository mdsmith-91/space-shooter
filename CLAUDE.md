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

*Main Menu:*
- W/S or ↑/↓: Navigate menu
- ENTER: Select option

*In Game:*
- WASD or Arrow keys: Move ship
- SPACE: Shoot laser
- ESC: Pause/Resume (shows pause menu)
- R: Restart after game over

## Code Architecture

**Game Loop Structure**:
- Event handling (pygame events, keyboard input)
- Game state updates (movement, collision detection, scoring)
- Rendering (draw stars, ship, asteroids, lasers, explosions, UI)

**Key Components**:
- **Ship**: Player-controlled spaceship with WASD/arrow key movement
- **Asteroids**: Randomly generated obstacles that break into smaller pieces
- **Lasers**: Projectiles fired by the player that destroy asteroids
- **Bosses**: Epic boss enemies that appear every 500 points and stay on screen until defeated
  - Three movement patterns: sine wave, circular, and figure-8
  - Orbit around a center position instead of moving off-screen
- **Power-ups**: 7 types (shield, rapid fire, spread shot, double damage, magnet, time slow, nuke)
- **Explosions**: Visual effects with particle systems
- **Stars**: Parallax scrolling background for visual depth
- **Menu System**: Main menu with Play, Highscores, and Exit options
- **High Score System**: Top 10 leaderboard stored in `data/high_score.txt`

**Collision Detection**:
- Ship-asteroid: Circular collision detection using distance formula
- Laser-asteroid: Rectangle-based collision detection

**State Management**:
- `game_state`: Tracks current screen ("menu", "playing", "game_over", "highscores")
- `game_over`: Boolean flag for game over state
- `paused`: Boolean flag for pause state
- `name_input_active`: Controls high score name entry flow
- Power-up timers and states for all active power-ups
- Combo system with timeout tracking

## File Persistence

- `data/high_score.txt`: Stores top 10 high scores, one per line
- Format: `{score}:{player_name}` (e.g., "14455:Michael")
- The `data/` directory is auto-created on first run
- Scores are automatically sorted and limited to top 10
- File is read on startup and written when a new high score qualifies

## Development Notes

- pygame uses a standard game loop pattern: event handling → update → render → clock tick
- The game includes a GitHub Actions workflow for automated Windows .exe builds
- PyInstaller is used for creating standalone executables
- **Resource Loading**: Uses `resource_path()` helper function (lines 15-24) to support both development and PyInstaller bundled executables
  - In development: Loads resources from current directory
  - In bundled .exe: Loads from PyInstaller's temporary extraction folder (`sys._MEIPASS`)
  - Critical for sound files to work in Windows .exe builds
  - All resource paths should use `resource_path("relative/path")` instead of direct paths

## Building for Distribution

See `BUILD.md` for detailed instructions on creating Windows executables. The project includes:
- `.github/workflows/build-windows.yml` - Automated CI/CD builds
- `build_windows.bat` - Manual build script for Windows systems
- `DISTRIBUTE_README.txt` - End-user instructions to include with the executable

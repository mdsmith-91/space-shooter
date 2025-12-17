# Space Shooter Game

A pygame-based space shooter where you control a ship, avoiding and shooting down asteroids.

## Features

- WASD movement controls
- Laser shooting mechanics with spacebar
- Explosion effects when asteroids are destroyed
- Parallax scrolling star field background
- High score system with name entry
- Progressive difficulty as you survive longer

## How to Play

**Run:** `python src/main.py`

**Controls:**
- `W` / `↑` - Move ship up
- `A` / `←` - Move ship left
- `S` / `↓` - Move ship down
- `D` / `→` - Move ship right
- `SPACE` - Shoot laser
- `R` - Restart after game over
- `ESC` - Exit game

## Setup

### Prerequisites
- Python 3.8+ (developed with Python 3.14.2)

### Installation

1. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── build-windows.yml    # GitHub Actions build workflow
├── src/
│   └── main.py                  # Space shooter game
├── BUILD.md                     # Build instructions
├── build_windows.bat            # Windows build script
├── DISTRIBUTE_README.txt        # Instructions for end users
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Technical Details

### Game Architecture
- Event-driven game loop using pygame
- Circular collision detection for ship-asteroid interactions
- Rectangle-based collision for laser-asteroid hits
- Persistent high score storage in `high_score.txt`
- Parallax scrolling background for visual depth

## Building for Distribution

Want to share the game with others who don't have Python installed?

### Windows Executable

See [BUILD.md](BUILD.md) for detailed instructions on creating a standalone Windows .exe file.

**Quick Start (on Windows):**
```cmd
build_windows.bat
```

**Using GitHub Actions:**
Push to GitHub and the workflow will automatically build Windows executables for you.

## Development

Built with:
- **pygame-ce** (Community Edition) - Game engine and graphics
- **Python 3.14.2** - Programming language

## License

Educational/Learning purposes

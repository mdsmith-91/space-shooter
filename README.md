# Python Learning Projects

A collection of Python projects for learning and practice, featuring a space shooter game and a GUI calculator.

## Projects

### 1. Ship Obstacle Avoidance Game
A pygame-based space shooter where you control a ship, avoiding and shooting down asteroids.

**Features:**
- WASD movement controls
- Laser shooting mechanics
- Explosion effects
- Scrolling star field background
- High score system with name entry
- Progressive difficulty

**Run:** `python src/main.py`

**Controls:**
- `WASD` - Move ship
- `SPACE` - Shoot laser
- `R` - Restart after game over
- `ESC` - Exit game

### 2. GUI Calculator
A tkinter-based calculator with a blue themed interface.

**Features:**
- Basic arithmetic operations (+, -, ×, ÷)
- Percentage calculations
- Sign toggle
- Clear function

**Run:** `python gui_calculator.py`

## Setup

### Prerequisites
- Python 3.14.2 (or compatible version)

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
├── src/
│   └── main.py          # Space shooter game
├── gui_calculator.py    # Calculator application
├── high_score.txt       # Game high score storage
├── requirements.txt     # Python dependencies
├── CLAUDE.md           # AI assistant instructions
└── README.md           # This file
```

## Technical Details

### Game Architecture
- Event-driven game loop using pygame
- Circular collision detection for ship-asteroid interactions
- Rectangle-based collision for laser-asteroid hits
- Persistent high score storage in `high_score.txt`

### Calculator Implementation
- Single class design using tkinter
- Immediate execution model (non-RPN)
- State management for operations and display

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
- pygame-ce (Community Edition)
- tkinter (included with Python)

## License

Educational/Learning purposes

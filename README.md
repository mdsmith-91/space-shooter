# Space Shooter Game

An action-packed pygame-based space shooter where you control a ship, blast asteroids, collect power-ups, and battle epic bosses!

## Features

### Core Gameplay
- **Dual control schemes**: WASD or Arrow keys for movement
- **Laser combat**: Shoot lasers with spacebar to destroy asteroids
- **Lives system**: Start with 3 lives and temporary invulnerability after taking damage
- **Breaking asteroids**: Large and medium asteroids split into smaller pieces when destroyed
- **Rotating asteroids**: Visual rotation effects with detailed crater graphics
- **Progressive difficulty**: Game speeds up and spawns more asteroids as you survive longer
- **Combo system**: Chain asteroid kills for score multipliers (up to 8x!)
- **Pause/Resume**: Press P to pause the game

### Power-Ups
Collect power-ups dropped by destroyed asteroids:
- **Shield**: Absorbs one hit from asteroids or bosses
- **Rapid Fire**: Shoot lasers faster for a limited time
- **Spread Shot**: Fire 3 lasers at once in a spread pattern
- **Double Damage**: Deal 2x damage and earn 2x points
- **Magnet**: Attract nearby power-ups automatically
- **Time Slow**: Slow down asteroids to half speed
- **Nuke**: Instantly destroy all asteroids and deal massive boss damage (rare!)

### Epic Boss Fights
- **Boss warnings**: Screen alerts before boss arrival
- **Multiple patterns**: Bosses use sine wave, circular, or figure-8 movement
- **Health bars**: Track boss health with visual indicators
- **Big rewards**: Defeating bosses grants 500 points and guaranteed power-ups

### Visual Effects
- **Particle systems**: Engine thrust, debris, laser trails, impact sparks, and power-up glows
- **Screen shake**: Dynamic camera shake on hits and explosions
- **Explosion animations**: Multi-layered explosions with transparency
- **Parallax scrolling**: Multi-depth star field background

### Audio
- **Sound effects**: Laser shots, explosions, hits, power-up collection, shield activation
- **Background music**: Looping soundtrack (when sound files are present)
- **Boss warnings**: Special audio cue for boss encounters

### Persistence
- **High score system**: Save your best score with your name
- **Persistent storage**: High scores saved to `high_score.txt`

## How to Play

**Run:** `python src/main.py`

**Controls:**
- `W` / `↑` - Move ship up
- `A` / `←` - Move ship left
- `S` / `↓` - Move ship down
- `D` / `→` - Move ship right
- `SPACE` - Shoot laser
- `P` - Pause/Resume game
- `R` - Restart after game over
- `ESC` - Exit game (when game over)

**Gameplay Tips:**
- **Combo chains**: Keep destroying asteroids quickly to build your combo multiplier
- **Power-up priority**: Shield and Spread Shot are great for survival; Double Damage for high scores
- **Boss strategy**: Use power-ups during boss fights for maximum effectiveness
- **Breaking asteroids**: Large asteroids split into smaller ones - clear them quickly!
- **Lives management**: You have 3 lives with brief invulnerability after each hit
- **Score milestones**: Bosses appear every 500 points - prepare accordingly!

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
├── sounds/                      # Sound effects and music (optional)
│   ├── laser.wav
│   ├── explosion.wav
│   ├── explosion_big.wav
│   ├── hit.wav
│   ├── powerup.wav
│   ├── shield.wav
│   ├── boss_warning.wav
│   └── music.wav
├── src/
│   └── main.py                  # Main game file (1800+ lines)
├── BUILD.md                     # Build instructions for Windows .exe
├── build_windows.bat            # Automated Windows build script
├── CLAUDE.md                    # Project guidance for Claude Code
├── DISTRIBUTE_README.txt        # End-user instructions for .exe
├── high_score.txt               # Persistent high score storage
├── requirements.txt             # Python dependencies (pygame-ce)
└── README.md                    # This file
```

## Technical Details

### Game Architecture
- **Event-driven game loop**: 60 FPS using pygame clock
- **Object-oriented design**: Separate classes for Ship, Asteroid, Boss, Laser, PowerUp, Explosion, Star, and Particle
- **Collision detection**:
  - Circular detection for ship-asteroid and ship-boss collisions
  - Rectangle-based detection for laser-asteroid and laser-boss hits
- **State management**: Game state, power-up timers, combo system, boss spawning
- **Particle system**: Dynamic particle generation for visual effects
- **Screen effects**: Camera shake with configurable intensity and duration

### Key Game Mechanics
- **Asteroid breaking**: Large/medium asteroids split into 2-3 smaller pieces with spread velocities
- **Boss spawn system**: Bosses appear every 500 points with warning sequences
- **Combo multipliers**: 1x → 2x → 3x → 5x → 8x scoring based on kill chains
- **Power-up duration**: Most power-ups last 5 seconds (300 frames at 60 FPS)
- **Difficulty scaling**: Asteroid spawn rate and speed increase over time (max 3x)
- **Invulnerability**: 2 seconds (120 frames) after taking damage
- **Sound system**: Graceful degradation - game runs silently if sound files missing

### Data Persistence
- **High score storage**: `{score}:{player_name}` format in `high_score.txt`
- **File handling**: Exception-safe I/O with fallback defaults

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

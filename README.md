# Space Shooter Game

An action-packed pygame-based space shooter where you control a ship, blast asteroids, collect power-ups, and battle epic bosses!

## What's New in v1.3

**Gameplay Improvements:**
- 🎯 **Score-based difficulty** - Difficulty now scales with your performance at milestones (100, 250, 500+)
- 💰 **5x better scoring** - Asteroids worth 10-25 points (up from 2-5) for more rewarding gameplay
- ⏱️ **Extended combos** - 3-second window (up from 2) makes combos more forgiving
- 🔄 **Power-up stacking** - Collecting duplicates extends duration up to 2x (14 seconds max)
- 💪 **Longer power-ups** - Most now last 7 seconds (up from 5) for better value
- 🎲 **5 boss patterns** - Added zigzag and spiral movements for more variety
- 📈 **Scaling bosses** - Boss health increases with difficulty (15-45 HP) for late-game challenge

**Balance Changes:**
- Double damage now correctly splits asteroids (was breaking them completely)
- Nuke damage to bosses reduced from 5 to 3 HP for better balance
- Shield still lasts 10 seconds while combat power-ups increased to 7 seconds

**Bug Fixes:**
- Fixed crash when ship collides with asteroids during iteration
- Fixed high score file corruption from special characters in names
- Fixed shield sound effect playing incorrect audio

**Performance:**
- Optimized font rendering (no more per-frame creation)
- Added collision detection early-exit for 50% fewer checks
- Smoother 60 FPS even with many power-ups on screen

## Features

### Core Gameplay
- **Dual control schemes**: WASD or Arrow keys for movement
- **Laser combat**: Shoot lasers with spacebar to destroy asteroids
- **Lives system**: Start with 3 lives and temporary invulnerability after taking damage
- **Breaking asteroids**: Large and medium asteroids split into smaller pieces when destroyed
- **Rotating asteroids**: Visual rotation effects with detailed crater graphics
- **Skill-based difficulty**: Difficulty scales with your score milestones (100, 250, 500, 1000+), not just time
- **Combo system**: Chain asteroid kills for score multipliers (up to 8x!) with 3-second window
- **Rewarding scoring**: Asteroids worth 10-25 points based on size for satisfying progression
- **Pause menu**: Press ESC to pause with options to Resume or return to Main Menu

### Menu System & UI
- **Main menu**: Professional title screen with Play, Highscores, Options, and Exit
- **Top 10 leaderboard**: View the best players and their scores
- **Options menu**: Adjust audio settings (volume and mute) accessible from main menu or pause menu
- **Pause menu**: Quick access to resume, options, or return to main menu during gameplay
- **Keyboard navigation**: Full WASD/Arrow key navigation throughout all menus
- **Visual feedback**: Highlighted selections and smooth menu transitions

### Power-Ups
Collect power-ups dropped by destroyed asteroids (all last 7 seconds except Shield at 10 seconds):
- **Shield**: Absorbs one hit from asteroids or bosses (10 seconds)
- **Rapid Fire**: Shoot lasers faster for a limited time (7 seconds)
- **Spread Shot**: Fire 3 lasers at once in a spread pattern (7 seconds)
- **Double Damage**: Deal 2x damage and earn 2x points (7 seconds)
- **Magnet**: Attract nearby power-ups automatically (7 seconds)
- **Time Slow**: Slow down asteroids to half speed (7 seconds)
- **Nuke**: Instantly destroy all asteroids and deal heavy boss damage (rare!)
- **Stacking**: Collecting the same power-up extends its duration up to 2x maximum (14 seconds for most)

### Epic Boss Fights
- **Boss warnings**: Screen alerts before boss arrival
- **5 unique patterns**: Bosses use sine wave, circular, figure-8, zigzag, or spiral movement patterns
- **Scaling difficulty**: Boss health increases with your difficulty level (15-45 HP)
- **Health bars**: Track boss health with visual indicators
- **Stay and fight**: Bosses remain on screen until defeated - no running away!
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
- **Volume control**: Adjustable volume slider (0-100%) in Options menu
- **Mute toggle**: Quick mute/unmute option for all audio
- **Settings persistence**: Audio preferences saved and restored between sessions

### Persistence
- **Top 10 leaderboard**: Compete for a spot on the high score board
- **Persistent storage**: High scores saved to `data/high_score.txt`
- **Audio settings**: Volume and mute preferences saved to `data/settings.txt`
- **Auto-save**: Scores and settings automatically saved

## How to Play

**Run:** `python src/main.py`

The game starts with a main menu where you can:
- **Play** - Start a new game
- **Highscores** - View the top 10 players
- **Options** - Adjust audio settings (volume and mute)
- **Exit** - Quit the game

**Controls:**

*Main Menu & Highscores:*
- `W`/`S` or `↑`/`↓` - Navigate options
- `ENTER` - Select option
- `ESC` - Return to menu (from highscores)

*Options Menu:*
- `W`/`S` or `↑`/`↓` - Navigate between Volume and Mute options
- `A`/`D` or `←`/`→` - Adjust volume slider or toggle mute
- `ENTER` - Toggle mute (when mute option is selected)
- `ESC` - Return to previous menu

*In Game:*
- `W` / `↑` - Move ship up
- `A` / `←` - Move ship left
- `S` / `↓` - Move ship down
- `D` / `→` - Move ship right
- `SPACE` - Shoot laser
- `ESC` - Open pause menu (Resume, Options, or Main Menu)
- `R` - Restart after game over

**Gameplay Tips:**
- **Combo chains**: You have 3 seconds between kills to maintain your combo - stay aggressive!
- **Power-up stacking**: Collecting duplicate power-ups extends their duration - grab them all!
- **Power-up priority**: Shield and Spread Shot are great for survival; Double Damage for high scores
- **Boss strategy**: Bosses get tougher as difficulty increases - save your best power-ups
- **Breaking asteroids**: Large asteroids split into smaller ones and are worth more points (25 vs 10)
- **Lives management**: You have 3 lives with brief invulnerability after each hit
- **Score milestones**: Difficulty increases at 100, 250, 500, 1000+ points - skill-based progression!

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
├── data/                        # Game save data (auto-created)
│   ├── high_score.txt           # Top 10 high scores
│   └── settings.txt             # Audio settings (volume, mute)
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
│   └── main.py                  # Main game file (2000+ lines)
├── BUILD.md                     # Build instructions for Windows .exe
├── build_windows.bat            # Automated Windows build script
├── CLAUDE.md                    # Project guidance for Claude Code
├── DISTRIBUTE_README.txt        # End-user instructions for .exe
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
- **Resource loading**: PyInstaller-compatible `resource_path()` helper for bundled executables

### Key Game Mechanics
- **Asteroid breaking**: Large/medium asteroids split into 2-3 smaller pieces with spread velocities
- **Asteroid scoring**: Points scale by size - Large: 25pts, Medium: 15pts, Small: 10pts
- **Boss spawn system**: Bosses appear every 500 points with warning sequences; stay on screen until defeated
- **Boss movement**: 5 unique patterns - sine wave, circular, figure-8, zigzag, and spiral
- **Boss scaling**: Health increases with difficulty level (15 HP at 1.0x → 45 HP at 3.0x difficulty)
- **Combo multipliers**: 1x → 2x → 3x → 5x → 8x scoring based on kill chains (3-second window)
- **Power-up duration**: Most power-ups last 7 seconds (420 frames), Shield lasts 10 seconds (600 frames)
- **Power-up stacking**: Collecting duplicates extends duration up to 2x maximum (14/20 seconds)
- **Difficulty scaling**: Score-based progression at milestones (100, 250, 500, 1000, 2000+) up to 3x max
- **Invulnerability**: 2 seconds (120 frames) after taking damage
- **Sound system**: Graceful degradation with PyInstaller support - game runs silently if sound files missing
- **Performance optimizations**: Font caching and collision detection early-exit for smooth 60 FPS

### Data Persistence
- **High score storage**: Top 10 scores stored in `data/high_score.txt` (one per line)
- **Settings storage**: Audio preferences stored in `data/settings.txt`
- **File formats**:
  - High scores: `{score}:{player_name}` per line, sorted descending
  - Settings: `volume:{0.0-1.0}` and `muted:{true/false}` per line
- **Auto-creation**: `data/` directory created automatically on first run
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

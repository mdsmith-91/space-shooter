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

*Options Menu:*
- W/S or ↑/↓: Navigate between Volume and Mute
- A/D or ←/→: Adjust volume or toggle mute
- ENTER: Toggle mute
- ESC: Return to previous menu

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
  - Scoring: Large (25pts), Medium (15pts), Small (10pts)
- **Lasers**: Projectiles fired by the player that destroy asteroids
- **Bosses**: Epic boss enemies that appear every 2500 points (v1.4) and stay on screen until defeated
  - Five movement patterns: sine wave, circular, figure-8, zigzag, and spiral
  - Health scales with difficulty level (15 HP at 1.0x → 45 HP at 3.0x)
  - Orbit around a center position instead of moving off-screen
- **Power-ups**: 7 types (shield, rapid fire, spread shot, double damage, magnet, time slow, nuke)
  - Duration: Most last 7 seconds (420 frames), Shield lasts 10 seconds (600 frames)
  - Stacking: Collecting duplicates extends duration up to 2x maximum
- **Explosions**: Visual effects with particle systems
- **Stars**: Parallax scrolling background for visual depth
- **Menu System**: Main menu with Play, Highscores, Options, and Exit
  - Pause menu with Resume, Options, and Main Menu
  - Options menu with volume slider and mute toggle
- **High Score System**: Top 10 leaderboard stored in `data/high_score.txt`
- **Settings System**: Audio preferences (volume, mute) stored in `data/settings.txt`

**Collision Detection**:
- Ship-asteroid: Circular collision detection using distance formula
- Laser-asteroid: Rectangle-based collision detection

**State Management**:
- `game_state`: Tracks current screen ("menu", "playing", "game_over", "highscores", "options")
- `game_over`: Boolean flag for game over state
- `paused`: Boolean flag for pause state
- `name_input_active`: Controls high score name entry flow
- `previous_state`: Tracks which menu opened the options (for navigation back)
- `options_selected`: Index for options menu navigation (0=volume, 1=mute)
- `volume`: Float (0.0-1.0) for audio volume percentage
- `muted`: Boolean flag for mute state
- `difficulty_level`: Float (1.0-3.0) that increases at score milestones
- `score`: Current score used to determine difficulty progression
- Power-up timers and states for all active power-ups (stack up to 2x duration)
- Combo system with 2-second timeout (COMBO_TIMEOUT = 120 frames, reduced in v1.4 for skill-based play)
- Combo multipliers: [1, 2, 3, 5, 8, 10] - up to 10x at combo 6+ (v1.4 added 10x tier)

## File Persistence

- `data/high_score.txt`: Stores top 10 high scores, one per line
  - Format: `{score}:{player_name}` (e.g., "14455:Michael")
  - Scores are automatically sorted and limited to top 10
  - File is read on startup and written when a new high score qualifies
- `data/settings.txt`: Stores audio settings, one per line
  - Format: `volume:{0.0-1.0}` and `muted:{true/false}`
  - File is read on startup and written when settings change
  - Settings apply to both music and all sound effects
- The `data/` directory is auto-created on first run

## Recent Changes (v1.4)

**Critical Bug Fixes**:
- Fixed music volume not applying on startup (line 1017): Removed conditional check that prevented volume initialization
- Fixed nuke power-up ignoring combo multipliers (lines 1349-1359): Now applies combo bonuses to nuke asteroid destruction
- Player name length now enforced (MAX_NAME_LENGTH = 15): Prevents UI overflow issues

**Performance Optimizations**:
- Reduced laser particle spawn rate by 50% (line 1517-1518): Uses random chance check to halve particle count
- Optimized time slow implementation (lines 322-334, 1536-1538): Asteroid.update() now accepts time_scale parameter, eliminating wasteful velocity save/restore operations every frame
- Added MAX_ASTEROIDS enforcement when breaking asteroids (lines 1662-1665, 1759-1762): Prevents performance degradation from asteroid spawning cascades

**Architecture Improvements**:
- **PowerUpManager class** (lines 705-778): New centralized power-up management system
  - Replaces 36+ lines of repetitive timer code with elegant class-based design
  - Methods: update(), activate(), is_active(), get_timer()
  - Manages all power-up states, timers, and stacking logic in one place
- Refactored Game class to use PowerUpManager throughout collision detection, UI rendering, and activation logic
- Removed 10 individual power-up state variables, replaced with single manager instance (line 932)

**Code Quality**:
- Added constants for magic numbers (lines 102-104): TIME_SLOW_MULTIPLIER, MAGNET_PULL_SPEED, NUKE_BOSS_DAMAGE
- Removed unused variables: difficulty_timer and DIFFICULTY_INCREASE_INTERVAL constant
- All magic numbers now have descriptive constant names for better maintainability

**Balance Changes**:
- Boss spawn interval increased from 500 to 2500 points (line 122): Compensates for 5x asteroid scoring increase in v1.3
- Difficulty milestones extended to 100,000 points (lines 1430-1431): 21 milestones from 0 to 100K with 0.1 increments, caps at 3.0x speed
- Combo timeout reduced from 180 to 120 frames (line 131): 2 seconds instead of 3, making combos more skill-based
- Difficulty increment reduced from 0.2 to 0.1 per milestone (line 1434): Smoother, more gradual difficulty curve
- Combo cap increased from 8x to 10x (line 132): Added 6th multiplier level for sustained skilled play
- Added difficulty display on HUD (lines 2139-2143): Shows "Speed: X.Xx" multiplier in golden color at (20, 90)

**Performance Impact**:
- 50% reduction in particle generation
- Eliminated 6-12 velocity operations per asteroid per frame during time slow
- Cleaner code architecture with ~60 lines removed, ~80 added for better functionality

## Recent Changes (v1.3)

**Critical Bug Fixes**:
- Fixed iterator modification crash in ship-asteroid collision (line 1685-1723): Now uses mark-and-remove pattern
- Fixed file injection vulnerability in high score names (lines 1185, 946): Rejects colons and newlines
- Fixed shield sound effect (lines 272-290): `take_damage()` now returns tuple `(game_over, shield_absorbed)`

**Gameplay Balance**:
- Asteroid scoring increased 5x: Line 306 changed from `radius/10` to `radius/2`
- Double damage now splits asteroids: Removed `and not self.double_damage_active` check at line 1603
- Combo timeout extended: Line 131 changed from 120 to 180 frames (3 seconds)
- Nuke boss damage reduced: Line 1291 changed from 5 to 3 damage
- Score-based difficulty: Lines 1391-1397 now use milestone array instead of frame counter
- Power-up duration increased: Line 100 changed from 300 to 420 frames (7 seconds)
- Boss health scaling: Boss.__init__ (line 452) now accepts difficulty_level parameter
- Boss spawn passes difficulty: Line 1421 calls `Boss(pattern, self.difficulty_level)`

**New Features**:
- Boss patterns expanded: Added "zigzag" (lines 506-513) and "spiral" (lines 515-522) patterns
- Power-up stacking: Lines 1286-1317 now add duration and cap at 2x maximum
- Pattern list updated: Line 1437 includes all 5 patterns

**Performance Optimizations**:
- Font caching: PowerUp class pre-renders text in `__init__` (lines 654-657), uses cached in `draw()` (lines 676-683)
- Collision early-exit: Lines 1606-1607 and 1661-1662 skip already-removed lasers

## Development Notes

- pygame uses a standard game loop pattern: event handling → update → render → clock tick
- The game includes a GitHub Actions workflow for automated Windows .exe builds
- PyInstaller is used for creating standalone executables
- **Resource Loading**: Uses `resource_path()` helper function (lines 15-24) to support both development and PyInstaller bundled executables
  - In development: Loads resources from current directory
  - In bundled .exe: Loads from PyInstaller's temporary extraction folder (`sys._MEIPASS`)
  - Critical for sound files to work in Windows .exe builds
  - All resource paths should use `resource_path("relative/path")` instead of direct paths
- **Audio Settings**:
  - `load_settings()` reads settings from file on game startup
  - `save_settings()` writes settings to file when changed
  - `apply_volume()` applies current volume/mute to pygame.mixer.music and all Sound objects
  - Volume changes take effect immediately via `apply_volume()` call
- **Difficulty System** (v1.4):
  - Uses score milestones [0, 400, 1000, 2000, 3500, 5500, 8000, 11000, 15000, 20000, 26000, 33000, 41000, 50000, 60000, 71000, 83000, 90000, 95000, 98000, 100000]
  - Difficulty increases by 0.1 per milestone, capped at 3.0x at 100,000 points
  - Affects asteroid spawn rate, speed, and boss health
  - Much more gradual progression compared to v1.3
- **Power-up Stacking** (v1.3):
  - Collecting same power-up adds to timer instead of replacing
  - Capped at 2x base duration (14 seconds for most, 20 for shield)
  - Prevents timer replacement, rewards collection

## Building for Distribution

See `BUILD.md` for detailed instructions on creating Windows executables. The project includes:
- `.github/workflows/build-windows.yml` - Automated CI/CD builds
- `build_windows.bat` - Manual build script for Windows systems
- `DISTRIBUTE_README.txt` - End-user instructions to include with the executable

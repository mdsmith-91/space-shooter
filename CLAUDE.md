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
- Keyboard: W/S or ↑/↓ to navigate, ENTER to select
- Controller: D-pad or analog stick to navigate, A/✕ to select

*Options Menu:*
- Keyboard: W/S or ↑/↓ to navigate, A/D or ←/→ to adjust, ENTER to toggle mute
- Controller: D-pad to navigate/adjust, A/✕ to toggle mute
- ESC or B/○: Return to previous menu

*In Game:*
- Keyboard: WASD or Arrow keys to move, SPACE to shoot
- Controller: Analog stick or D-pad to move, A/✕ or RT to shoot
- ESC or START: Pause/Resume (shows pause menu)
- R: Restart after game over (keyboard only)

## Code Architecture

**Game Loop Structure**:
- Event handling (pygame events, keyboard input)
- Game state updates (movement, collision detection, scoring)
- Rendering (draw stars, ship, asteroids, lasers, explosions, UI)

**Key Components**:
- **Ship**: Player-controlled spaceship with keyboard/controller movement (v1.5.3: controller support; v1.5: enhanced graphics with thrusters, lights, panel details)
- **Asteroids**: Randomly generated obstacles that break into smaller pieces (v1.5: irregular polygons, 4 rock types, 3D craters, minerals)
  - Scoring: Large (25pts), Medium (15pts), Small (10pts)
- **Lasers**: Projectiles fired by the player that destroy asteroids (v1.5: fading trail effects)
- **Bosses**: Epic boss enemies that appear every 2500 points (v1.4) and stay on screen until defeated
  - Five movement patterns: sine wave, circular, figure-8, zigzag, and spiral
  - Health scales with difficulty level (15 HP at 1.0x → 45 HP at 3.0x)
  - Orbit around a center position instead of moving off-screen
- **Power-ups**: 7 types (shield, rapid fire, spread shot, double damage, magnet, time slow, nuke)
  - Duration: Most last 7 seconds (420 frames), Shield lasts 10 seconds (600 frames)
  - Stacking: Collecting duplicates extends duration up to 2x maximum (v1.5: pulsing glow halos)
- **Explosions**: Visual effects with particle systems (v1.5: 8-layer radial gradients, particle bursts)
- **Stars**: Parallax scrolling background for visual depth (v1.5: twinkling effect)
- **Nebula Clouds** (v1.5): Procedural multi-layered background clouds
- **Score Popups** (v1.5): Floating animated score numbers on asteroid destruction
- **Distortion Waves** (v1.5): Screen-wide ripple effects for boss spawn and nuke
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
- `joystick`: Pygame joystick object if controller detected, None otherwise (v1.5.3)
- `controller_deadzone`: Float (0.2) threshold for analog stick input (v1.5.3)
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

## Recent Changes (v1.5.4)

**Documentation Update** - Complete documentation overhaul

**Updates**:
- Updated README.md with comprehensive v1.5.3 controller support documentation
- Updated DISTRIBUTE_README.txt for end users with controller instructions
- Updated CLAUDE.md with detailed technical documentation of controller implementation
- Added version history sections (v1.5.1, v1.5.2, v1.5.3) to all documentation
- Enhanced control schemes documentation for both keyboard and controller inputs
- Improved user-facing instructions across all documentation files

**Files Updated**:
- README.md: Added v1.5.3 controller support section, detailed controls tables
- DISTRIBUTE_README.txt: Added controller controls section for end users
- CLAUDE.md: Added v1.5.3 technical documentation with line numbers
- All docs now consistently reflect version history and features

## Recent Changes (v1.5.3)

**Controller/Gamepad Support** - Full input device support added

**New Features**:
- **Controller detection**: Auto-detects and initializes joystick/gamepad on startup (lines 9, 1863-1868)
- **Analog stick movement**: Ship.update() accepts joystick parameter with deadzone support (lines 247-285)
- **D-pad navigation**: Hat motion events for menu navigation (lines 2207-2242)
- **Button mapping**:
  - Button 0 (A/Cross): Shoot and menu selection (lines 2165-2186)
  - Button 1 (B/Circle): Back and pause actions (lines 2187-2200)
  - Button 9 (START): Pause/resume game (lines 2201-2205)
  - Right trigger (Axis 5): Alternative shoot control (lines 2645-2647)
- **Seamless input**: Keyboard and controller can be used simultaneously
- **Full menu support**: Controller navigation works in all menus and options

**Technical Details**:
- Joystick initialized via pygame.joystick.init() on game start
- Ship class updated to handle joystick input with configurable deadzone (0.2 default)
- Game class stores joystick instance and handles JOYBUTTONDOWN and JOYHATMOTION events
- Controller name printed to console on detection for debugging

**Code Changes**:
- Added joystick parameter throughout Ship movement code
- Implemented controller event handling in process_events()
- Updated all menu navigation to support D-pad input
- Added trigger-based shooting alongside button-based shooting

## Recent Changes (v1.5.2)

**Performance Optimizations and Bug Fixes**

**Improvements**:
- Performance optimizations for smoother gameplay at 60 FPS
- General code cleanup and refinements
- Bug fixes for edge cases discovered in testing
- Minor stability improvements

## Recent Changes (v1.5.1)

**Code Quality Improvements**

**Changes**:
- Code cleanup and better organization
- Additional performance improvements building on v1.5.0
- Minor bug fixes and stability enhancements
- Documentation refinements

## Recent Changes (v1.5.0)

**Massive Graphics Overhaul** - ~900 lines of new visual code added

**New Visual Classes**:
- **ScorePopup** (lines 1234-1296): Floating animated score numbers
  - Pop-in animation, black outline for readability
  - Size scales with score magnitude
  - Transparent background rendering
- **NebulaCloud** (lines 1299-1365): Procedural background nebula clouds
  - Multi-layered cloud rendering
  - Parallax scrolling effect
  - Random colors and sizes
- **DistortionWave** (lines 1368-1411): Screen-wide ripple effects
  - Expanding concentric rings
  - Triggered on boss spawn and nuke activation
  - Fading alpha animation

**Enhanced Ship Graphics** (lines 231-436):
- Subtle ship aura/glow matching ship color
- Animated engine thrusters with pulsing blue glow
- Surface panel details for mechanical appearance
- Blinking navigation lights (green top, red bottom)
- Glass-effect cockpit with specular highlights
- Wing detail lines for structural definition
- Visible weapon port at nose
- 4-layer gradient shading with metallic highlights

**Enhanced Asteroid Graphics** (lines 503-744):
- **Irregular polygon shapes**: 8-12 sided unique polygons (not circles!)
- **4 rock types**: Gray stone, brown rock, blue-gray, tan/beige with custom color schemes
- **Surface texture patches**: Color variation for realistic appearance
- **3D craters**: 3-6 craters per asteroid with depth shading and rim lighting
- **Enhanced cracks**: 3-6 cracks with variable width (1-2 pixels)
- **Mineral sparkles**: 30% of asteroids have 3-8 twinkling mineral points
- **Better lighting**: Rim lighting adapted to each rock type
- **Defined outlines**: Polygon edge rendering

**Enhanced Explosion Effects** (lines 1010-1119):
- 8-layer radial gradients (was 5 simple circles)
- 8-12 explosion particles with organic burst patterns
- Color evolution: white/yellow flash → orange → dark red
- Bright center flash for impact moment
- Dynamic brightness based on explosion progress
- 50% faster growth rate (1.5 vs 1.0)

**Enhanced Particle System** (lines 867-936):
- Multi-shape support: circle, star, square
- `draw_star()` and `draw_square()` methods
- Shape parameter in constructor

**New Visual Effects**:
- **Vignette overlay**: Pre-rendered radial gradient darkening screen edges
- **Motion blur**: Ghost trails on asteroids (3 positions tracked)
- **Twinkling stars**: Brightness variation using sine wave
- **Hexagonal shield**: Honeycomb pattern with rotating hexagons (lines 437-469)
- **Laser trails**: 5-segment fading trails (lines 790-837)

**UI/HUD Enhancements**:
- Holographic scan lines across screen
- Health bar pulsing when critically low (1 life)
- Power-up progress bars showing remaining duration
- Combo scale pulse and screen edge glow
- Dynamic color themes (blue → purple → red based on score)
- Boss fight red tint overlay
- Score popups integrated in collision detection

**Graphics Constants Added** (lines 152-183):
- `SCORE_POPUP_LIFETIME`, `SCORE_POPUP_RISE_SPEED`
- `NEBULA_COUNT`, `NEBULA_MIN_SIZE`, `NEBULA_MAX_SIZE`, `NEBULA_COLORS`
- `DISTORTION_MAX_RADIUS`, `DISTORTION_LIFETIME`
- `COMBO_PULSE_SPEED`, `SCAN_LINE_SPEED`
- `THEME_BLUE_MAX`, `THEME_PURPLE_MAX`, `THEME_RED_MIN`
- `HEXAGON_RADIUS`, `HEXAGON_LAYERS`
- `LASER_TRAIL_LENGTH`, `MOTION_BLUR_POSITIONS`

**New Game Instance Variables**:
- `score_popups[]`, `nebula_clouds[]`, `distortion_waves[]`
- `vignette_surface`, `theme_color`, `scan_line_offset`
- `previous_combo`, `previous_lives`

**Performance Impact**:
- All enhancements maintain 60 FPS
- Pre-rendered vignette for efficiency
- Optimized particle counts
- Clean class-based architecture

**Code Size**: ~3200 lines (was ~2300) - 40% increase for visual polish

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

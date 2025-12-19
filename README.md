# Space Shooter Game 🚀

An action-packed pygame-based space shooter where you control a ship, blast asteroids, collect power-ups, and battle epic bosses!

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5%2B-green)](https://pyga.me/)
[![License](https://img.shields.io/badge/license-Educational-orange)](LICENSE)

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [What's New](#-whats-new)
- [Features](#-features)
- [Controls](#-controls)
- [Gameplay Tips](#-gameplay-tips)
- [Installation](#-installation)
- [Building for Distribution](#-building-for-distribution)
- [Technical Details](#-technical-details)
- [Development](#-development)

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/mdsmith-91/space-shooter.git
cd space-shooter

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the game
python src/main.py
```

**That's it!** Use WASD/Arrows to move, SPACE to shoot, ESC to pause.

---

## 🎉 What's New

### Version 1.5.0 (Latest) - Graphics Overhaul

**🎨 Massive Visual Enhancement - Every aspect dramatically improved!**

**Ship Graphics:**
- ✨ **Subtle ship aura** - Glowing outline matches ship color
- 🔥 **Animated engine thrusters** - Pulsing blue glow at rear (changes to orange when damaged)
- 🔧 **Surface panel details** - Mechanical segments and structural definition
- 💡 **Blinking navigation lights** - Green (top) and red (bottom) aircraft-style lights
- 🪟 **Glass-effect cockpit** - Multi-layer rendering with bright specular highlights
- ✈️ **Wing detail lines** - Structural definition for engineered look
- 🎯 **Visible weapon port** - Shows where lasers fire from
- 🌟 **Better gradient shading** - 4-layer gradients with metallic highlights

**Asteroid Graphics:**
- 🔷 **Irregular shapes** - Each asteroid is a unique 8-12 sided polygon (no more circles!)
- 🌈 **4 rock types** - Gray stone, brown rock, blue-gray, tan/beige with custom color schemes
- 🎭 **Surface texturing** - Color patches simulate realistic rock variation
- 🕳️ **3D craters** - Deep craters with proper depth shading and rim lighting
- ⚡ **Enhanced crack systems** - 3-6 visible cracks with variable width
- ✨ **Mineral sparkles** - 30% of asteroids have twinkling mineral deposits
- 💡 **Better lighting** - Rim lighting adapted to each rock type's colors
- 🔷 **Defined outlines** - Clear shape definition

**Explosion Effects:**
- 💥 **Smooth radial gradients** - 8-layer explosion rendering (was 5)
- 🎆 **8-12 explosion particles** - Organic burst patterns that slow over time
- 🌟 **Color evolution** - White/yellow flash → orange → dark red progression
- ⚡ **Bright center flash** - Realistic impact brightness in first frames
- 🎨 **Dynamic coloring** - Changes from bright core to darker edges
- 🔥 **50% faster growth rate** - More impactful visual feedback

**Score Popups:**
- 📈 **Pop-in animation** - Numbers start small and quickly grow to full size
- 🖤 **Black outline** - 8-direction outline for perfect readability
- 📏 **Size scaling** - Larger scores get bigger, more impactful numbers
- ✨ **Transparent background** - No yellow rectangles, just clean text
- 🎯 **Bold font rendering** - Crisp, clear score feedback

**New Visual Systems:**
- 🌌 **Procedural nebula clouds** - 5 multi-layered background clouds with parallax
- 💫 **Distortion waves** - Expanding ripple effects on boss spawn and nuke
- 🎭 **Enhanced particles** - Star, square, and circle shapes for variety
- 🖼️ **Vignette overlay** - Darkened screen edges for cinematic focus
- 👻 **Motion blur** - Ghost trails on fast-moving asteroids
- 🌟 **Twinkling stars** - Background stars vary in brightness
- 🔷 **Hexagonal shield** - Honeycomb pattern with rotating hexagons

**UI Enhancements:**
- 📺 **Holographic scan lines** - Animated lines across entire screen
- ❤️ **Health bar pulse** - Red pulsing warning when critically low (1 life)
- 📊 **Power-up progress bars** - Visual bars show remaining duration
- 🎯 **Combo effects** - Scale pulse + screen edge glow that intensifies
- 🎨 **Dynamic color themes** - Background shifts Blue→Purple→Red with score
- 🔴 **Boss fight atmosphere** - Subtle red tint overlay during boss battles

**Performance Impact:** All graphics enhancements maintain smooth 60 FPS!

<details>
<summary><b>Version 1.4.0 Changelog</b></summary>

**Major Performance & Architecture Improvements:**
- 🏗️ **PowerUpManager class** - Elegant new architecture replaces 60+ lines of repetitive code
- ⚡ **50% fewer particles** - Laser trail particles reduced for smoother performance
- 🚀 **Optimized time slow** - Rewrote asteroid update system for better efficiency
- 🛡️ **Smart asteroid limiting** - Prevents performance issues when asteroids break

**Critical Bug Fixes:**
- 🔊 Fixed music volume not applying on game startup
- 💥 Fixed nuke power-up ignoring combo multipliers
- 📝 Fixed potential UI overflow from long player names

**Gameplay Balance:**
- 👾 **Bosses every 2500 points** (was 500) - compensates for v1.3's 5x scoring increase
- 🎯 **Smoother difficulty curve** - Extended to 100K points with 0.1 increments
- ⏱️ **Harder combos** - 2-second window (down from 3) rewards skilled play
- 🔥 **10x combo multiplier** - New tier for sustained 6+ kill chains (was 8x max)
- 📊 **Difficulty HUD display** - See your current speed multiplier on screen

</details>

<details>
<summary><b>Version 1.3.0 Changelog</b></summary>

**Gameplay Improvements:**
- 🎯 Score-based difficulty scaling at milestones
- 💰 5x better scoring (10-25 points per asteroid)
- 🔄 Power-up stacking up to 2x duration
- 💪 Longer power-ups (7 seconds, shield 10 seconds)
- 🎲 5 boss movement patterns (added zigzag and spiral)
- 📈 Scaling boss health (15-45 HP based on difficulty)

**Bug Fixes:**
- Fixed ship-asteroid collision crash
- Fixed high score file corruption
- Fixed shield sound effect

**Performance:**
- Optimized font rendering
- Collision detection early-exit
- Smooth 60 FPS with many effects

</details>

---

## ✨ Features

### 🎮 Core Gameplay
- **Dual control schemes** - WASD or Arrow keys
- **Lives system** - 3 lives with invulnerability frames after damage
- **Dynamic difficulty** - Scales from 0 to 100K points across 21 milestones
- **Combo system** - Chain kills for up to **10x multiplier** (2-second window)
- **Smart scoring** - Asteroids worth 10-25 points based on size
- **Asteroid breaking** - Large/medium asteroids split into smaller pieces
- **Difficulty display** - Live speed multiplier shown on HUD

### 👾 Epic Boss Fights
- **Boss spawn** - Every 2500 points with screen warnings
- **5 unique patterns** - Sine wave, circular, figure-8, zigzag, spiral
- **Scaling difficulty** - Health increases from 15 HP to 45 HP
- **Stay and fight** - Bosses orbit on screen until defeated
- **Big rewards** - 500 points + guaranteed power-up drops

### 💪 Power-Ups
Collect rotating colored squares dropped by destroyed asteroids:

| Power-Up | Duration | Effect |
|----------|----------|--------|
| 🟢 **Shield** | 10 sec | Absorbs one hit from any source |
| 🟡 **Rapid Fire** | 7 sec | Shoot lasers faster |
| 🟣 **Spread Shot** | 7 sec | Fire 3 lasers at once |
| 🩷 **Double Damage** | 7 sec | Deal 2x damage, earn 2x points |
| 🟣 **Magnet** | 7 sec | Attract power-ups automatically |
| 🔵 **Time Slow** | 7 sec | Slow asteroids to half speed |
| 🔴 **Nuke** | Instant | Destroy all asteroids (rare!) |

**Stacking:** Collecting the same power-up extends duration up to 2x max (14/20 seconds)

### 🎨 Visual & Audio
- **Advanced ship graphics** - Animated thrusters, panel details, navigation lights, glass cockpit
- **Realistic asteroids** - Irregular polygon shapes, 4 rock types, 3D craters, mineral sparkles
- **Smooth explosions** - 8-layer radial gradients with particle bursts
- **Particle systems** - Multiple shapes (star, square, circle), engine thrust, debris, laser trails
- **Screen effects** - Vignette overlay, motion blur, chromatic aberration, distortion waves
- **UI polish** - Holographic scan lines, progress bars, combo effects, dynamic themes
- **Procedural backgrounds** - Nebula clouds, twinkling stars, parallax scrolling
- **Score popups** - Animated floating numbers with outlines
- **Screen shake** - Dynamic camera shake on hits and explosions
- **Sound effects** - Lasers, explosions, hits, power-ups, shields, boss warnings
- **Background music** - Looping soundtrack (when sound files present)
- **Volume controls** - Adjustable volume (0-100%) and mute toggle in Options

### 📊 Menus & Persistence
- **Main menu** - Play, Highscores, Options, Exit
- **Pause menu** - Resume, Options, Main Menu (press ESC in-game)
- **Options menu** - Volume slider and mute toggle
- **Top 10 leaderboard** - High scores saved to `data/high_score.txt`
- **Settings persistence** - Audio preferences saved to `data/settings.txt`
- **Full keyboard navigation** - WASD/Arrows throughout all menus

---

## 🎮 Controls

### Main Menu / Highscores / Pause Menu
| Key | Action |
|-----|--------|
| `W` `S` or `↑` `↓` | Navigate menu options |
| `ENTER` | Select option |
| `ESC` | Go back / Resume (in pause menu) |

### Options Menu
| Key | Action |
|-----|--------|
| `W` `S` or `↑` `↓` | Navigate between Volume and Mute |
| `A` `D` or `←` `→` | Adjust volume / Toggle mute |
| `ENTER` | Toggle mute |
| `ESC` | Return to previous menu |

### In-Game
| Key | Action |
|-----|--------|
| `W` or `↑` | Move ship up |
| `A` or `←` | Move ship left |
| `S` or `↓` | Move ship down |
| `D` or `→` | Move ship right |
| `SPACE` | Shoot laser |
| `ESC` | Open pause menu |
| `R` | Restart (after game over) |

---

## 💡 Gameplay Tips

### Mastering Combos
- 🎯 **2-second window** - You have 2 seconds between kills to maintain combo
- 🔥 **10x multiplier** - Reach 6+ consecutive kills for maximum scoring
- ⚡ **Stay aggressive** - Chain kills quickly for massive point bonuses

### Power-Up Strategy
- 🟢 **Shield + Spread Shot** - Best for survival
- 🩷 **Double Damage** - Maximum scoring potential
- 🎁 **Stack duplicates** - Extend duration up to 2x for sustained power
- 🧲 **Magnet synergy** - Makes collecting other power-ups easier

### Boss Encounters
- 👾 **Spawn every 2500 points** - Save your best power-ups
- 💪 **Scale with difficulty** - Later bosses have 3x more health
- 🎯 **Orbit patterns** - Learn the 5 movement patterns to predict positions
- 🔴 **Nuke strategy** - Deals 3 damage (20% of base health)

### Difficulty Management
- 📊 **Watch the HUD** - Speed multiplier shows asteroid velocity
- 🎢 **21 milestones** - Difficulty scales smoothly from 0 to 100K points
- 🎯 **3.0x maximum** - Speed caps at 100,000 points
- 💎 **Large asteroids** - Worth 25 points but split into smaller ones

### Survival Tips
- 💚 **3 lives total** - Brief invulnerability after each hit
- 🌟 **Break asteroids** - Large (25pts) → Medium (15pts) → Small (10pts)
- 🏃 **Keep moving** - Stationary targets are easy hits
- 👀 **Watch the right** - Asteroids spawn from the right side

---

## 📦 Installation

### Prerequisites
- **Python 3.8+** (developed with Python 3.14.2)
- **pip** (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/mdsmith-91/space-shooter.git
cd space-shooter
```

2. **Create virtual environment**
```bash
python3 -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

This installs **pygame-ce** (Community Edition) - a modern, actively maintained fork of pygame.

4. **Run the game**
```bash
python src/main.py
```

### Project Structure

```
space-shooter/
├── .github/
│   └── workflows/
│       └── build-windows.yml    # Automated Windows builds
├── data/                        # Auto-created on first run
│   ├── high_score.txt           # Top 10 high scores
│   └── settings.txt             # Audio settings
├── sounds/                      # Optional sound files
│   ├── laser.wav
│   ├── explosion.wav
│   ├── explosion_big.wav
│   ├── hit.wav
│   ├── powerup.wav
│   ├── shield.wav
│   ├── boss_warning.wav
│   └── music.wav
├── src/
│   └── main.py                  # Main game file (~3200 lines)
├── BUILD.md                     # Windows .exe build guide
├── build_windows.bat            # Windows build script
├── CLAUDE.md                    # AI assistant guidance
├── DISTRIBUTE_README.txt        # End-user instructions
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 📦 Building for Distribution

Want to share the game with users who don't have Python installed?

### Windows Executable

**Option 1: Automated (GitHub Actions)**
- Push to GitHub
- Workflow automatically builds Windows .exe
- Download from Actions artifacts or Releases

**Option 2: Manual Build (Windows only)**
```cmd
build_windows.bat
```
Find executable at `dist/SpaceShooter.exe`

**Detailed Instructions:** See [BUILD.md](BUILD.md)

---

## 🔧 Technical Details

### Architecture

**Game Loop (60 FPS)**
- Event handling → State updates → Rendering → Clock tick

**Classes**
- `Ship` - Player spaceship with enhanced graphics, movement, and damage
- `Asteroid` - Irregular polygon obstacles with realistic texturing and breaking mechanics
- `Boss` - Epic enemies with movement patterns and energy veins animation
- `Laser` - Player projectiles with fading trails
- `PowerUp` - Collectible enhancements with pulsing glow halos
- `PowerUpManager` - Centralized power-up state (v1.4)
- `Explosion` - Advanced particle-based effects with radial gradients
- `Star` - Twinkling parallax background elements
- `Particle` - Multi-shape particle system (circle, star, square)
- `ScorePopup` - Floating animated score notifications (v1.5)
- `NebulaCloud` - Procedural background cloud layers (v1.5)
- `DistortionWave` - Screen-wide ripple effects (v1.5)

**Collision Detection**
- Circular: Ship ↔ Asteroid, Ship ↔ Boss
- Rectangle: Laser ↔ Asteroid, Laser ↔ Boss
- Early-exit optimizations for performance

**State Management**
- Game states: menu, playing, game_over, highscores, options
- Power-up timers via PowerUpManager
- Combo system with 2-second timeout
- Boss spawning at 2500-point intervals

### Game Mechanics

**Scoring System**
- Small asteroids: 10 points
- Medium asteroids: 15 points
- Large asteroids: 25 points
- Boss defeat: 500 points
- Combo multipliers: 1x, 2x, 3x, 5x, 8x, 10x

**Difficulty Scaling**
- 21 milestones from 0 to 100,000 points
- 0.1 increment per milestone
- Caps at 3.0x speed multiplier
- Affects: asteroid speed, spawn rate, boss health

**Power-Up System**
- Base duration: 7 seconds (420 frames), Shield: 10 seconds (600 frames)
- Stacking: Up to 2x duration maximum
- Managed by PowerUpManager class (v1.4)

**Performance Optimizations**
- Font caching (pre-rendered text)
- Particle spawn reduction (50% fewer laser trails)
- Collision early-exit (skip already-removed objects)
- Optimized time slow (time_scale parameter vs velocity modification)
- MAX_ASTEROIDS limit enforcement

### Data Persistence

**High Scores** (`data/high_score.txt`)
- Format: `score:player_name` per line
- Top 10 scores, sorted descending
- Input sanitization (rejects colons/newlines)

**Settings** (`data/settings.txt`)
- Format: `volume:0.0-1.0` and `muted:true/false`
- Loaded on startup, saved on change
- Applies to all audio (music + sound effects)

**Resource Loading**
- `resource_path()` helper for PyInstaller compatibility
- Works in both development and bundled .exe
- Critical for sound files in distributed builds

---

## 👨‍💻 Development

### Built With
- **[pygame-ce](https://pyga.me/)** - Community Edition game engine
- **[Python 3.14.2](https://www.python.org/)** - Programming language
- **[PyInstaller](https://pyinstaller.org/)** - Executable bundling

### Code Quality
- Object-oriented design with clear separation of concerns
- ~3200 lines of well-commented Python
- PowerUpManager architecture for maintainability (v1.4)
- Advanced graphics systems with clean class architecture (v1.5)
- Named constants (no magic numbers)
- Exception-safe file I/O

### Contributing
This is a personal learning project, but feel free to:
- Report bugs via [GitHub Issues](https://github.com/mdsmith-91/space-shooter/issues)
- Fork and experiment
- Share your high scores!

---

## 📄 License

This project is for **educational and learning purposes**.

---

## 🎮 Have Fun!

Enjoy the game and good luck beating the high score! 🚀

**Repository:** [github.com/mdsmith-91/space-shooter](https://github.com/mdsmith-91/space-shooter)

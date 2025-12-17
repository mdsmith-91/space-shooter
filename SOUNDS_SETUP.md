# Sound Effects Setup Guide

## Quick Start (Recommended)

### Download the Kenney Sound Pack

1. **Download the pack:**
   - Go to: https://opengameart.org/sites/default/files/Digital_SFX_Set.zip
   - Or visit: https://opengameart.org/content/63-digital-sound-effects-lasers-phasers-space-etc
   - Download `Digital_SFX_Set.zip` (1.1 MB)

2. **Extract the ZIP file:**
   - You'll get a folder with 63 .wav files
   - Files are named like: `laser1.wav`, `powerUp1.wav`, etc.

3. **Copy files to your sounds folder:**
   ```
   Space-Shooter/
   └── sounds/
       ├── laser.wav          (pick your favorite laser sound)
       ├── explosion.wav      (pick an explosion sound)
       ├── explosion_big.wav  (pick a bigger explosion)
       ├── hit.wav            (pick a hit/damage sound)
       ├── powerup.wav        (pick a power-up sound)
       ├── shield.wav         (optional: shield sound)
       └── boss_warning.wav   (optional: warning sound)
   ```

## Recommended File Mapping

From the Kenney pack, I recommend these mappings:

| Your File | Kenney File | Use For |
|-----------|-------------|---------|
| `laser.wav` | `laser1.wav` or `laser7.wav` | Shooting lasers |
| `explosion.wav` | `explosion1.wav` | Asteroid destruction |
| `explosion_big.wav` | `explosion2.wav` | Boss defeat |
| `hit.wav` | `hit1.wav` or `zap1.wav` | Taking damage |
| `powerup.wav` | `powerUp1.wav` or `powerUp11.wav` | Collecting power-ups |
| `shield.wav` | `forceField_001.ogg` (if included) | Shield activation |
| `boss_warning.wav` | `lowDown.wav` | Boss warning |

## Alternative: Mixkit Sounds

If you prefer to download individual sounds from Mixkit:

1. Visit: https://mixkit.co/free-sound-effects/space-shooter/
2. Click individual sounds to preview
3. Click "Download Free SFX" for each one you like
4. Rename them to match the names above

## File Format

- **Supported formats**: `.wav` or `.ogg`
- **Recommended**: `.wav` for best compatibility
- **Size**: Keep files under 500KB each for best performance

## Testing

Once you've added the sound files, run the game:

```bash
source .venv/bin/activate
python src/main.py
```

You should hear:
- ✅ Laser sound when shooting (SPACE)
- ✅ Explosion when asteroids break
- ✅ Hit sound when you take damage
- ✅ Power-up sound when collecting items
- ✅ Big explosion when boss is defeated

## Troubleshooting

**Problem: No sound playing**
- Check that files are in the `sounds/` folder
- Make sure files are named correctly (case-sensitive!)
- Verify your system volume is up
- Check terminal for error messages

**Problem: "FileNotFoundError"**
- Files must be in `sounds/` folder relative to `src/main.py`
- Check file names match exactly (e.g., `laser.wav` not `Laser.wav`)

**Problem: Sound is distorted**
- Try a different sound file
- Some sounds may need volume adjustment in code

## Optional: Background Music

For background music:
1. Find a CC0 music track (try: https://opengameart.org/art-search-advanced?keys=&title=&field_art_tags_tid_op=or&field_art_tags_tid=&name=&field_art_type_tid%5B%5D=12&sort_by=count&sort_order=DESC)
2. Save as `sounds/music.ogg`
3. The code will automatically load and loop it

## License Info

**Kenney Sounds**: CC0 (Public Domain)
- Free to use commercially
- No attribution required (but appreciated!)
- Credit: "Kenney.nl" or "www.kenney.nl"

**Mixkit Sounds**: Mixkit License
- Free for commercial use
- Check individual sound licenses on their site

Enjoy your newly enhanced game! 🎮🔊

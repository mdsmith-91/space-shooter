# Building Windows Executable

Instructions for creating a standalone Windows executable of the Space Shooter game.

## Prerequisites

**You must build on a Windows system** (PyInstaller cannot cross-compile from macOS to Windows).

Options:
- Windows PC
- Windows VM (VirtualBox, Parallels, VMware)
- Cloud VM (AWS, Azure)
- GitHub Actions (see Method 2 below)

## Method 1: Manual Build on Windows

### 1. Install Python on Windows
Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)

### 2. Set Up Project on Windows

Transfer your project files to the Windows system:
```cmd
# Clone/copy the project
cd C:\path\to\project
```

### 3. Create Virtual Environment
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
pip install pyinstaller
```

### 5. Build the Executable

**Option A: One-file executable (easier distribution)**
```cmd
pyinstaller --onefile --windowed --name "SpaceShooter" --add-data "sounds;sounds" src/main.py
```

**Option B: One-folder (faster startup)**
```cmd
pyinstaller --windowed --name "SpaceShooter" --add-data "sounds;sounds" src/main.py
```

**Note:** The `--add-data "sounds;sounds"` flag includes sound effects and music in the executable. The game uses a PyInstaller-compatible `resource_path()` helper function to properly locate sound files in bundled executables. If you don't have a sounds folder, you can omit this flag - the game will run silently but otherwise work perfectly.

**Flags explained:**
- `--onefile` - Packages everything into a single .exe file
- `--windowed` - Hides the console window (use `--console` for debugging)
- `--name` - Sets the executable name

### 6. Find Your Executable

The executable will be in:
- **One-file**: `dist/SpaceShooter.exe`
- **One-folder**: `dist/SpaceShooter/SpaceShooter.exe` (distribute entire folder)

### 7. Test on Windows

Run the executable on a clean Windows system without Python to verify it works.

### 8. Distribute

- **One-file**: Just share the .exe file
- **One-folder**: Zip the entire `dist/SpaceShooter/` folder

## Method 2: Automated Build with GitHub Actions

### 1. Create GitHub Repository

Push your code to GitHub (if not already):
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/space-shooter.git
git push -u origin main
```

### 2. Create Workflow File

Create `.github/workflows/build-windows.yml` (see separate instructions)

### 3. Trigger Build

Push to GitHub or manually trigger the workflow. The .exe will be available as a downloadable artifact.

## Common Issues

### Issue: "Failed to execute script" on Windows
- Make sure pygame-ce is properly bundled
- Try `--console` flag to see error messages
- Add hidden imports: `--hidden-import=pygame`

### Issue: No sound in bundled .exe
- **FIXED**: The game now includes a `resource_path()` helper that properly locates resources
- Ensure `--add-data "sounds;sounds"` is in the PyInstaller command
- The sounds folder must exist and be properly included in the build

### Issue: Large file size
- Normal for PyInstaller (30-50 MB for pygame apps)
- Use UPX compression: `pyinstaller --onefile --windowed --upx-dir=C:\path\to\upx src/main.py`

### Issue: Antivirus flags the .exe
- Common false positive with PyInstaller
- Code sign your executable (requires certificate)
- Build with `--debug=all` to help antivirus analysis

## Advanced: Custom Icon

```cmd
pyinstaller --onefile --windowed --icon=icon.ico --name "SpaceShooter" --add-data "sounds;sounds" src/main.py
```

Create `icon.ico` from an image using an online converter.

## File Size Optimization

1. Use `--onedir` instead of `--onefile` (smaller, faster startup)
2. Exclude unnecessary modules:
   ```cmd
   pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy src/main.py
   ```
3. Use UPX compression (download from upx.github.io)

## Distribution Checklist

- [ ] Test on clean Windows system (no Python)
- [ ] Test on Windows 10 and 11
- [ ] Include README with controls
- [ ] Consider adding installer (Inno Setup, NSIS)
- [ ] Virus scan the executable
- [ ] Document system requirements

## System Requirements for Players

- Windows 10/11 (64-bit)
- ~50 MB free disk space
- DirectX 9.0c or later (usually pre-installed)

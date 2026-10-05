# File Organizer
**Developed by Abdelrahman Awad**

Organize a directory by moving files into category folders (Images, Documents, Audio, Video, Archives, Code, Fonts, Other) based on extension.

## Features
- Categorizes files safely (skips folders)
- Handles name collisions (adds '(1)', '(2)', ...)
- `--dry-run` to preview without moving
- Optionally include dotfiles via `--include-hidden`

## Quick Start
```bash
python3 file_organizer.py ~/Downloads --dry-run
python3 file_organizer.py ~/Downloads
```

## Example Output
```
Moved report.pdf -> Documents/
Moved song.mp3 -> Audio/
Moved photo.jpg -> Images/
Processed 3 files.
```

## Dev
- MIT License
- CI: Black/Ruff/Pytest

#!/usr/bin/env python3
# File Organizer - categorize files in a directory by extension.
# Safety: moves only regular files; skips hidden files by default; supports --dry-run.

import argparse, shutil
from pathlib import Path

CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"],
    "Archives": [".zip", ".tar", ".gz", ".bz2", ".7z"],
    "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rb", ".php", ".html", ".css", ".json", ".xml", ".yml", ".yaml", ".sh", ".ipynb"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Other": []
}

def guess_category(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if exts and ext in exts:
            return cat
    return "Other"

def organize(folder: Path, include_hidden=False, dry_run=False):
    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Folder does not exist: {folder}")
    moved = []
    for p in folder.iterdir():
        if not p.is_file():
            continue
        if not include_hidden and p.name.startswith("."):
            continue
        cat = guess_category(p)
        target_dir = folder / cat
        target = target_dir / p.name
        if dry_run:
            moved.append((p, target))
        else:
            target_dir.mkdir(exist_ok=True)
            final = target
            i = 1
            while final.exists():
                final = target_dir / f"{p.stem} ({i}){p.suffix}"
                i += 1
            import shutil
            shutil.move(str(p), str(final))
            moved.append((p, final))
    return moved

def main():
    ap = argparse.ArgumentParser(description="Organize files in a directory by type.")
    ap.add_argument("folder", help="Folder to organize")
    ap.add_argument("--include-hidden", action="store_true", help="Include hidden files (starting with .)")
    ap.add_argument("--dry-run", action="store_true", help="Show what would happen without moving files")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    moved = organize(folder, include_hidden=args.include_hidden, dry_run=args.dry_run)
    if args.dry_run:
        for src, dst in moved:
            print(f"[DRY-RUN] {src.name} -> {dst.parent.name}/")
    else:
        for src, dst in moved:
            print(f"Moved {src.name} -> {dst.parent.name}/")
    print(f"Processed {len(moved)} files.")

if __name__ == "__main__":
    main()

import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "file_organizer.py"

def run(args, cwd):
    res = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    return res.stdout

def test_dry_run_and_move(tmp_path: Path):
    # Create sample files
    (tmp_path / "a.txt").write_text("doc", encoding="utf-8")
    (tmp_path / "b.jpg").write_bytes(b"jpg")
    (tmp_path / "c.mp3").write_bytes(b"mp3")

    # Dry run
    out = run([str(tmp_path), "--dry-run"], tmp_path)
    assert "[DRY-RUN]" in out

    # Real run
    out = run([str(tmp_path)], tmp_path)
    assert "Processed 3 files." in out
    assert (tmp_path / "Documents" / "a.txt").exists()
    assert (tmp_path / "Images" / "b.jpg").exists()
    assert (tmp_path / "Audio" / "c.mp3").exists()

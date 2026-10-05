import subprocess, sys
from pathlib import Path

def run(args, cwd):
    res = subprocess.run([sys.executable, "password_checker.py", *args], cwd=cwd, capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    return res.stdout

def test_scoring(tmp_path: Path):
    for fname in ["password_checker.py", "common_passwords.txt"]:
        src = Path.cwd() / fname
        (tmp_path / fname).write_text(src.read_text(), encoding="utf-8")
    out = run(["Hello123!thisIsGood"], tmp_path)
    assert "Strength:" in out and "Score:" in out

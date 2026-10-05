import subprocess, sys
from pathlib import Path

def run(args, cwd):
    res = subprocess.run([sys.executable, "network_scanner.py", *args], cwd=cwd, capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    return res.stdout

def test_dry_run(tmp_path: Path):
    src = Path.cwd() / "network_scanner.py"
    (tmp_path / "network_scanner.py").write_text(src.read_text(), encoding="utf-8")
    out = run(["192.168.1.0/30", "--dry-run"], tmp_path)
    assert "Total hosts: " in out

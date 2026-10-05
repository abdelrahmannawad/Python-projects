import subprocess, sys
from pathlib import Path
from datetime import date

def run(cmd, cwd):
    res = subprocess.run([sys.executable, "wellness_logger.py", *cmd],
                         cwd=cwd, capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    return res.stdout

def test_end_to_end(tmp_path: Path):
    # copy script into temp dir
    repo = tmp_path
    src = Path(__file__).resolve().parent.parent / "wellness_logger.py"
    (repo / "wellness_logger.py").write_text(src.read_text(), encoding="utf-8")

    # init
    out = run(["init"], repo)
    assert "Initialized" in out or "Log already exists" in out

    # log example
    out = run(["log", "--date", date.today().isoformat(),
               "--workouts", "Swim + Lift",
               "--calories-eaten", "2800",
               "--sleep-hours", "7.5",
               "--water-liters", "3.0",
               "--calories-burned", "600"], repo)
    assert ("Logged" in out) or ("Updated" in out)

    # view/today shouldn't error
    run(["view", "--days", "7"], repo)
    run(["today"], repo)

    # summary prints aggregates
    out = run(["summary", "--days", "7"], repo)
    assert "Summary for last" in out

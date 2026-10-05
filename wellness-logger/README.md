# Wellness Logger (Local CLI App)
**Developed by Abdelrahman Awad**

A zero-setup, privacy-first command-line app to log daily wellness metrics locally in a CSV.

## Features
- Log: workouts (text), calories eaten, calories burned (optional), sleep hours, water liters
- View: show last N days in a clean table
- Summary: totals/averages over a time window (e.g., last 7/30 days)
- Today: show today's entry
- Delete-last: remove your most recent row
- Export: copy CSV to output/ for backup (e.g., open in Excel/Sheets)
- 100% offline, no accounts, no uploads

## Why
- Data stays on your machine (CSV you own)
- Fast to use from terminal
- Easy to extend or analyze later

## Quick Start
```bash
# (optional) make executable on Mac/Linux
chmod +x wellness_logger.py

# initialize storage
python3 wellness_logger.py init

# log today
python3 wellness_logger.py log --workouts "Swim + Lift" --calories-eaten 2800 --sleep-hours 7.5 --water-liters 3.0 --calories-burned 600

# view & summary
python3 wellness_logger.py view --days 7
python3 wellness_logger.py summary --days 7

# export a dated copy of your CSV
python3 wellness_logger.py export
```

## CLI Reference
```
usage: wellness_logger.py [-h] [--version] {init,log,today,view,summary,delete-last,export} ...

positional arguments:
  {init,log,today,view,summary,delete-last,export}
    init           Create data/ and an empty CSV if missing
    log            Add or overwrite a daily entry
    today          Show today's entry
    view           View last N days (default 7)
    summary        Summary stats for last N days (default 7)
    delete-last    Delete the most recent entry
    export         Export CSV copy to output/

options:
  -h, --help       show this help message and exit
  --version        show program's version number and exit
```

### Log command
```
python3 wellness_logger.py log   --date 2025-11-13   --workouts "Swim 5x100 BR + Lift"   --calories-eaten 2800   --sleep-hours 7.5   --water-liters 3.0   --calories-burned 600
```

## Data Format
CSV stored at `data/wellness_log.csv`:
| date       | workouts             | calories_burned | calories_eaten | sleep_hours | water_liters |
|------------|----------------------|-----------------|----------------|-------------|--------------|
| 2025-11-13 | Swim + Lift          | 600             | 2800           | 7.5         | 3.0          |

- Re-logging the same `date` overwrites the previous row (one row per day).

## Dev
- MIT License
- `pyproject.toml` for metadata + Black/Ruff configs
- `tests/` with a basic end-to-end test
- GitHub Actions CI: lint + tests on every push/PR

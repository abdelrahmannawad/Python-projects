#!/usr/bin/env python3
# Wellness Logger - local CLI app (no uploads).
# Tracks per day: workouts, calories_burned, calories_eaten, sleep_hours, water_liters.

import argparse, csv, sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict

__version__ = "1.0.0"

ROOT = Path(__file__).parent.resolve()
DATA_DIR = ROOT / 'data'
OUT_DIR = ROOT / 'output'
LOG_CSV = DATA_DIR / 'wellness_log.csv'

FIELDNAMES = ['date','workouts','calories_burned','calories_eaten','sleep_hours','water_liters']

def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_date(s: str) -> str:
    return datetime.strptime(s, '%Y-%m-%d').date().isoformat()

def read_all() -> List[Dict[str,str]]:
    if not LOG_CSV.exists():
        return []
    with LOG_CSV.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_all(rows: List[Dict[str,str]]) -> None:
    ensure_dirs()
    with LOG_CSV.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def cmd_init(_args):
    ensure_dirs()
    if LOG_CSV.exists():
        print(f'Log already exists at {LOG_CSV}')
        return
    write_all([])
    print(f'Initialized new log at {LOG_CSV}')

def _to_entry(args) -> dict:
    d = args.date or date.today().isoformat()
    try:
        d = parse_date(d)
    except Exception:
        print('ERROR: --date must be YYYY-MM-DD'); sys.exit(1)
    workouts = (args.workouts or '').strip()
    try:
        cb = int(args.calories_burned) if args.calories_burned is not None else 0
        ce = int(args.calories_eaten)
        sh = float(args.sleep_hours)
        wl = float(args.water_liters)
    except Exception as e:
        print('ERROR parsing number:', e); sys.exit(1)
    if cb < 0 or ce < 0 or sh < 0 or wl < 0:
        print('ERROR: negative values are not allowed.'); sys.exit(1)
    return {'date': d, 'workouts': workouts, 'calories_burned': cb, 'calories_eaten': ce, 'sleep_hours': sh, 'water_liters': wl}

def cmd_log(args):
    ensure_dirs()
    rows = read_all()
    e = _to_entry(args)
    replaced = False
    for i, r in enumerate(rows):
        if r['date'] == e['date']:
            rows[i] = {k: str(e[k]) for k in FIELDNAMES}
            replaced = True
            break
    if not replaced:
        rows.append({k: str(e[k]) for k in FIELDNAMES})
        rows.sort(key=lambda r: r['date'])
    write_all(rows)
    print(('Updated' if replaced else 'Logged'), e)

def _print_table(rows: List[Dict[str,str]]):
    if not rows:
        print('(no rows)'); return
    cols = FIELDNAMES
    widths = [max(len(c), max(len(str(r.get(c,''))) for r in rows)) for c in cols]
    fmt = ' | '.join('{:<'+str(w)+'}' for w in widths)
    print(fmt.format(*cols))
    print('-+-'.join('-'*w for w in widths))
    for r in rows:
        print(fmt.format(*(str(r.get(c,'')) for c in cols)))

def cmd_today(_args):
    today = date.today().isoformat()
    rows = read_all()
    for r in reversed(rows):
        if r['date'] == today:
            _print_table([r]); return
    print('No entry for today yet. Use: log --calories-eaten ... --sleep-hours ... --water-liters ...')

def _in_last_n_days(rows: List[Dict[str,str]], n: int) -> List[Dict[str,str]]:
    cutoff = date.today() - timedelta(days=n-1)
    out = []
    for r in rows:
        try:
            d = datetime.strptime(r['date'], '%Y-%m-%d').date()
        except Exception:
            continue
        if d >= cutoff:
            out.append(r)
    return out

def cmd_view(args):
    n = args.days or 7
    rows = read_all()
    subset = _in_last_n_days(rows, n)
    _print_table(subset)

def cmd_summary(args):
    n = args.days or 7
    rows = _in_last_n_days(read_all(), n)
    if not rows:
        print(f'No data in the last {n} days.'); return
    def _sum(col):
        s = 0.0
        for r in rows:
            try: s += float(r[col])
            except: pass
        return s
    def _avg(col):
        return _sum(col)/len(rows)
    totals = {
        'entries': len(rows),
        'total_calories_burned': int(_sum('calories_burned')),
        'total_calories_eaten': int(_sum('calories_eaten')),
        'total_sleep_hours': round(_sum('sleep_hours'), 2),
        'total_water_liters': round(_sum('water_liters'), 2),
    }
    avgs = {
        'avg_calories_burned': round(_avg('calories_burned'), 1),
        'avg_calories_eaten': round(_avg('calories_eaten'), 1),
        'avg_sleep_hours': round(_avg('sleep_hours'), 2),
        'avg_water_liters': round(_avg('water_liters'), 2),
    }
    print(f'Summary for last {n} days')
    print('-'*32)
    for k,v in totals.items(): print(f'{k:>24}: {v}')
    for k,v in avgs.items(): print(f'{k:>24}: {v}')

def cmd_delete_last(_args):
    rows = read_all()
    if not rows:
        print('Nothing to delete.'); return
    last = rows[-1]
    rows = rows[:-1]
    write_all(rows)
    print('Deleted last entry:', last)

def cmd_export(_args):
    ensure_dirs()
    if not LOG_CSV.exists():
        print('Nothing to export; log is empty.'); return
    target = OUT_DIR / f'wellness_log_export_{date.today().isoformat()}.csv'
    target.write_bytes(LOG_CSV.read_bytes())
    print(f'Exported to {target}')

def main(argv=None):
    parser = argparse.ArgumentParser(description='Wellness Logger – local, zero-setup daily wellness tracking to CSV.')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_init = sub.add_parser('init', help='Create data/ and an empty CSV if missing')
    p_init.set_defaults(func=cmd_init)

    p_log = sub.add_parser('log', help='Add or overwrite a daily entry')
    p_log.add_argument('--date', help='YYYY-MM-DD (default: today)')
    p_log.add_argument('--workouts', required=False, default='', help="Free text, e.g., 'Swim + Lift'")
    p_log.add_argument('--calories-burned', dest='calories_burned', required=False, default=0, help='Integer (default 0)')
    p_log.add_argument('--calories-eaten', dest='calories_eaten', required=True, help='Integer')
    p_log.add_argument('--sleep-hours', dest='sleep_hours', required=True, help='Float, e.g., 7.5')
    p_log.add_argument('--water-liters', dest='water_liters', required=True, help='Float, e.g., 3.0')
    p_log.set_defaults(func=cmd_log)

    p_today = sub.add_parser('today', help="Show today's entry")
    p_today.set_defaults(func=cmd_today)

    p_view = sub.add_parser('view', help='View last N days (default 7)')
    p_view.add_argument('--days', type=int, default=7)
    p_view.set_defaults(func=cmd_view)

    p_sum = sub.add_parser('summary', help='Summary stats for last N days (default 7)')
    p_sum.add_argument('--days', type=int, default=7)
    p_sum.set_defaults(func=cmd_summary)

    p_del = sub.add_parser('delete-last', help='Delete the most recent entry')
    p_del.set_defaults(func=cmd_delete_last)

    p_exp = sub.add_parser('export', help='Export CSV copy to output/')
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    main()

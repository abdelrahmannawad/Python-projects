#!/usr/bin/env python3
# Password Checker - score password strength using simple rules + common list check.

import argparse, re
from pathlib import Path

COMMON_FILE = Path(__file__).parent / "common_passwords.txt"

RULES = [
    ("length>=12", lambda s: len(s) >= 12),
    ("has_lower", lambda s: re.search(r"[a-z]", s) is not None),
    ("has_upper", lambda s: re.search(r"[A-Z]", s) is not None),
    ("has_digit", lambda s: re.search(r"\d", s) is not None),
    ("has_symbol", lambda s: re.search(r"[^\w\s]", s) is not None),
    ("not_common", lambda s: s.strip().lower() not in load_common()),
]

_common_cache = None
def load_common():
    global _common_cache
    if _common_cache is not None:
        return _common_cache
    if not COMMON_FILE.exists():
        _common_cache = set(["password","123456","qwerty","111111","12345678","abc123"])
        return _common_cache
    words = set()
    for line in COMMON_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip().lower()
        if line:
            words.add(line)
    _common_cache = words
    return _common_cache

def score_password(pw: str):
    checks = [(name, fn(pw)) for name, fn in RULES]
    score = sum(1 for _, ok in checks if ok)
    strength = "Weak"
    if score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    return score, strength, checks

def main():
    ap = argparse.ArgumentParser(description="Password strength checker")
    ap.add_argument("password", help="Password string to evaluate")
    args = ap.parse_args()

    score, strength, checks = score_password(args.password)
    print(f"Password: {args.password}")
    print(f"Score: {score}/{len(RULES)}")
    print(f"Strength: {strength}")
    for name, ok in checks:
        print(f" - {name}: {'OK' if ok else 'FAIL'}")

if __name__ == "__main__":
    main()

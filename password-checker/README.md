# Password Strength Checker
**Developed by Abdelrahman Awad**

Evaluate password strength using length and character-mix rules plus a check against a list of common passwords.

## Rules
- length>=12
- has_lower
- has_upper
- has_digit
- has_symbol
- not_common (compares against `common_passwords.txt` if present)

## Quick Start
```bash
python3 password_checker.py "Hello123!thisIsGood"
```

### Output Example
```
Password: Hello123!thisIsGood
Score: 6/6
Strength: Strong
 - length>=12: OK
 - has_lower: OK
 - has_upper: OK
 - has_digit: OK
 - has_symbol: OK
 - not_common: OK
```

## Dev
- MIT License
- CI: Black/Ruff/Pytest

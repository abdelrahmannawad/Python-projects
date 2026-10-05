# Python Projects

[![CI](https://github.com/abdelrahmannawad/Python-projects/actions/workflows/ci.yml/badge.svg)](https://github.com/abdelrahmannawad/Python-projects/actions/workflows/ci.yml)

Small, dependency-free Python command-line tools covering automation, security basics, and everyday utilities. Each project has its own folder with a README, license, and tests.

| Project | What it does | Try it |
|---|---|---|
| [file-organizer](file-organizer) | Sorts files in a folder into categories (Images, Documents, Audio, and more), with `--dry-run` and safe handling of name collisions. | `python3 file_organizer.py ~/Downloads --dry-run` |
| [password-checker](password-checker) | Scores password strength on length, character mix, and a common-passwords list. | `python3 password_checker.py "Hello123!thisIsGood"` |
| [simple-network-scanner](simple-network-scanner) | ICMP ping sweep over a subnet using concurrent pings. | `python3 network_scanner.py 192.168.1.0/30 --dry-run` |
| [wellness-logger](wellness-logger) | Logs daily workouts, sleep, water, and calories to a local CSV with summaries and export. | `python3 wellness_logger.py summary --days 7` |

## Requirements

Python 3.9 or newer. No third-party packages are needed to run the tools. Tests use `pytest`.

## Running the tests

```bash
cd file-organizer
pip install pytest
pytest -q
```

## Responsible use

The network scanner should only be used on networks you own or have permission to test.

## License

MIT. See the LICENSE file in each project.

# Simple Network Scanner
**Developed by Abdelrahman Awad**

A lightweight ICMP ping-sweep tool that scans a given subnet and lists reachable hosts.

## Features
- CIDR input (e.g., `192.168.1.0/24`)
- Multithreaded pinging with configurable `--workers`
- Cross-platform ping command
- `--dry-run` to preview IPs without pinging
- `--timeout` to tune per-host timeout

## Quick Start
```bash
# Preview which IPs will be scanned
python3 network_scanner.py 192.168.1.0/30 --dry-run

# Run a real scan (may require admin privileges on some systems)
python3 network_scanner.py 192.168.1.0/30 --workers 32 --timeout 1.0
```

## Notes
- ICMP replies can be blocked by firewalls; use `--dry-run` during testing/CI.
- Designed for educational and authorized use on networks you own or administer.

## Dev
- MIT License
- CI: Black/Ruff/Pytest

#!/usr/bin/env python3
# Simple Network Scanner - ICMP ping sweep over a subnet.
# Cross-platform friendly, with --dry-run and --timeout. Avoids raw sockets.

import argparse, ipaddress, platform, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_one(ip: str, timeout: float) -> bool:
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(int(timeout*1000)), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(int(timeout)), ip]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False

def scan_subnet(cidr: str, workers: int = 64, timeout: float = 1.0, dry_run: bool = False):
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = [str(h) for h in net.hosts()]
    if dry_run:
        return hosts
    alive = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(ping_one, ip, timeout): ip for ip in hosts}
        for fut in as_completed(futs):
            ip = futs[fut]
            if fut.result():
                alive.append(ip)
    return sorted(alive, key=lambda x: tuple(int(p) for p in x.split(".")))

def main():
    ap = argparse.ArgumentParser(description="Simple ICMP ping sweep over a subnet.")
    ap.add_argument("cidr", help="CIDR, e.g., 192.168.1.0/24")
    ap.add_argument("--workers", type=int, default=64, help="Max concurrent pings")
    ap.add_argument("--timeout", type=float, default=1.0, help="Per-host timeout in seconds")
    ap.add_argument("--dry-run", action="store_true", help="Just list the IPs that would be scanned")
    args = ap.parse_args()

    if args.dry_run:
        hosts = scan_subnet(args.cidr, dry_run=True)
        for ip in hosts:
            print(ip)
        print(f"Total hosts: {len(hosts)}")
    else:
        alive = scan_subnet(args.cidr, workers=args.workers, timeout=args.timeout)
        if alive:
            print("Alive hosts:")
            for ip in alive:
                print(f"  {ip}")
        else:
            print("No alive hosts detected (or blocked by firewall).")

if __name__ == "__main__":
    main()

import argparse
import asyncio
from typing import List


async def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if port is open on host."""
    try:
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except (OSError, asyncio.TimeoutError):
        return False


async def run_scanner(host: str, ports: List[int]) -> List[int]:
    open_ports = []
    for port in ports:
        if await scan_port(host, port):
            open_ports.append(port)
    return open_ports


def parse_ports(port_arg: str) -> List[int]:
    """Parse a port argument like '1-1024,8080'"""
    ports = set()
    for part in port_arg.split(','):
        if '-' in part:
            start, end = map(int, part.split('-', 1))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple asynchronous port scanner")
    parser.add_argument('host', help='Target host to scan')
    parser.add_argument('-p', '--ports', default='1-1024',
                        help='Ports to scan, e.g., "1-1024,8080"')
    parser.add_argument('-t', '--timeout', type=float, default=1.0,
                        help='Timeout per connection attempt (seconds)')
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    print(f"Scanning {args.host} on ports: {args.ports}...")

    open_ports = asyncio.run(run_scanner(args.host, ports))

    if open_ports:
        print("Open ports:", ', '.join(map(str, open_ports)))
    else:
        print("No open ports found")


if __name__ == '__main__':
    main()

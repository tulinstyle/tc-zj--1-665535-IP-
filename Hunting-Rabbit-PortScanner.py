import argparse
import socket
import time

import concurrent.futures
import ipaddress

def check_host_alive(host, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except Exception as e:
        return False

def scan_port(host, port, timeout, results):
    if check_host_alive(host, port, timeout):
        results.append(port)

def scan_host(host, port_range, timeout, results, verbose=False):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for port in parse_ports(port_range):
            futures.append(executor.submit(scan_port, host, port, timeout, open_ports))
        concurrent.futures.wait(futures)
    if open_ports:
        if verbose:
            print(f'{host} is alive')
            print(f'{host} has open ports: {", ".join(map(str, open_ports))}')
        results.append((host, open_ports))
    else:
        if verbose:
            print(f'{host} is not alive')

def scan_network(network, port_range, timeout, max_workers=32, verbose=False):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for host in ipaddress.IPv4Network(network):
            futures.append(executor.submit(scan_host, str(host), port_range, timeout, results, verbose=verbose))
        concurrent.futures.wait(futures)
    return results

def parse_ports(port_range):
    ports = []
    for item in port_range.split(','):
        if '-' in item:
            start, end = item.split('-')
            start = int(start)
            end = int(end)
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(item))
    return ports

parser = argparse.ArgumentParser(description='Hunting-Rabbit-PortScanner       author:浪飒')
max_port = 65535  # 最大端口号
default_ports = ','.join(map(str, range(1, max_port + 1)))
parser.add_argument('network', help='Network to scan (e.g. "192.168.0.1" or "192.168.0.0/24")')
parser.add_argument('-p', '--ports', default=default_ports,
                    help=f'Ports to scan (e.g. "80" or "1-{max_port}", default: %(default)s)')
parser.add_argument('-t', '--timeout', type=float, default=0.5,
                    help='TCP connection timeout in seconds (default: %(default)s)')
parser.add_argument('-w', '--workers', type=int, default=64,
                    help='Maximum number of worker threads for the scan (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

network = args.network
port_range = args.ports
timeout = args.timeout
max_workers = args.workers

start_time = time.time()

print(f'[*] Scanning network {network} ({port_range})...')

results = scan_network(network, port_range, timeout, max_workers=max_workers, verbose=args.verbose)

end_time = time.time()
elapsed_time = end_time - start_time

if results:
    print(f'[+] Found open ports on {len(results)} host(s):')
    for host, open_ports in results:
        print(f'    {host}: {", ".join(map(str, open_ports))}')
else:
    print('[-] No open ports found on any host.')

print(f'[+] Scan completed in {elapsed_time:.2f} seconds.')

import socket
import sys
import argparse
import concurrent.futures

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def format_port_results(results):
    output = "[*] Scan Results:\n"
    output += "{:<10} {:<15} {:<10}\n".format("Port", "Service", "Status")
    for port, service, banner, is_open in results:
        if is_open:
            output += f"{RED}{port:<10} {service:<15} Open{RESET}\n"
            if banner:
                lines = banner.split('\n')
                for line in lines:
                    output += f"{GREEN}    {line.strip()}{RESET}\n"
    return output

def get_banner(sock):
    try:
        sock.settimeout(2)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = 'unknown'
            banner = get_banner(sock)
            sock.close()
            return (port, service, banner, True)
        sock.close()
        return (port, '', '', False)
    except Exception as e:
        return (port, '', '', False)

def port_scanner(host, start_port, end_port):
    print(f"\n[*] Scanning {host} from port {start_port} to {end_port}\n")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {
            executor.submit(scan_port, host, port): port
            for port in range(start_port, end_port + 1)
        }

        total = end_port - start_port + 1
        completed = 0

        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            results.append(result)
            completed += 1
            sys.stdout.write(f"\r[+] Progress: {completed}/{total} ports scanned")
            sys.stdout.flush()

    print("\n")
    output = format_port_results(results)
    print(output)

    # Save to file
    with open("scan_results.txt", "w") as f:
        f.write(output)
    print("[*] Results saved to scan_results.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded Port Scanner")
    parser.add_argument("host", help="Target host or IP address")
    parser.add_argument("start_port", type=int, help="Start port")
    parser.add_argument("end_port", type=int, help="End port")

    args = parser.parse_args()

    port_scanner(args.host, args.start_port, args.end_port)

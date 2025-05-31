import subprocess
import ipaddress
import platform

def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", str(ip)]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def scan(ip_range):
    network = ipaddress.ip_network(ip_range, strict=False)
    print(f"\n[+] Scanning {ip_range}...\n")
    print("Available Devices:")
    print("-" * 30)
    for ip in network.hosts():
        if ping(ip):
            print(f"Host {ip} is online")

if __name__ == "__main__":
    target = input("Enter IP range (e.g., 192.168.29.0/24): ")
    scan(target)

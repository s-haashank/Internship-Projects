import requests
import threading

# Ask user to enter the domain
domain = input("Enter the target domain (e.g., youtube.com): ")

# Read subdomains from wordlist file
with open('subdomains.txt') as file:
    subdomains = file.read().splitlines()

# Shared list to store discovered subdomains
discovered_subdomains = []

# Lock for thread-safe operations
lock = threading.Lock()

# Function to check a single subdomain
def check_subdomain(subdomain):
    url = f'http://{subdomain}.{domain}'
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 400:
            print("[+] Discovered subdomain:", url)
            with lock:
                discovered_subdomains.append(url)
    except requests.RequestException:
        pass  # Skip subdomains that are unreachable

# Create and start threads
threads = []
for subdomain in subdomains:
    thread = threading.Thread(target=check_subdomain, args=(subdomain,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Write discovered subdomains to output file
with open("discovered_subdomains.txt", "w") as f:
    for subdomain in discovered_subdomains:
        print(subdomain, file=f)

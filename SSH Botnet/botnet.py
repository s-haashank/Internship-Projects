import os
import sys
import paramiko
from easygui import passwordbox
from termcolor import cprint

clients = []

def display_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\n--- SSH Botnet Menu ---")
    print("1. List Bots")
    print("2. Run Command")
    print("3. Add Client")
    print("4. Exit")

def connect(host, port, user, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=user, password=password)
        return ssh
    except Exception as e:
        cprint(f"[!] Error connecting to {host}: {e}", "red")
        return None

def send_command(session, cmd):
    stdin, stdout, stderr = session.exec_command(cmd)
    return stdout.read().decode()

def botnet_command():
    cmd = input("Enter command to run: ")
    if not clients:
        cprint("[!] No bots available.", "red")
        return
    for client in clients:
        host = client['host']
        session = client['session']
        print(f"\n--- [{host}] Output ---")
        try:
            output = send_command(session, cmd)
            print(output)
        except:
            cprint(f"[!] Error sending command to {host}", "red")

def add_client():
    host = input("Host: ")
    port = int(input("Port [default 22]: ") or 22)
    user = input("Username: ")
    password = passwordbox("Enter SSH password:")
    
    session = connect(host, port, user, password)
    if session:
        clients.append({'host': host, 'port': port, 'user': user, 'password': password, 'session': session})
        cprint(f"[+] {host} added successfully.", "green")
    else:
        cprint("[!] Failed to add bot.", "red")

while True:
    display_menu()
    choice = input(">> ")
    if choice == "1":
        if clients:
            for bot in clients:
                print(f"{bot['host']} - {bot['user']}@{bot['port']}")
        else:
            print("[!] No bots in list.")
    elif choice == "2":
        botnet_command()
    elif choice == "3":
        add_client()
    elif choice == "4":
        print("Exiting...")
        for bot in clients:
            bot['session'].close()
        break
    else:
        print("Invalid option!")

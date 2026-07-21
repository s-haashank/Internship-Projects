import socket
import time
//code
while True:
    try:
        s = socket.socket()
        s.connect((" 192.168.29.162", 9999))
        print("[+] Connected!")
        break
    except:
        print("[-] Retry in 3s...")
        time.sleep(3)

import socket
#code
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("0.0.0.0", 9999))
listener.listen(1)
print("[*] Listening...")
target, addr = listener.accept()
print(f"[+] Got connection from {addr}")

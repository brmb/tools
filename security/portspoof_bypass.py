import socket

def scan_port(host, port, protocol):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # Set a timeout of 5 seconds for the socket operation
        s.connect((host, port))

        if protocol == "FTP":
            s.send(b'USER anonymous\r\n')
            s.recv(1024)
            s.send(b'PASS anonymous\r\n')
            response = s.recv(1024)
            if "Login" in response.decode('utf-8') or "successful" in response.decode('utf-8'):
                print(f"[+] {port}/tcp {protocol} [Open]")
        elif protocol == "HTTP":
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)  # Set a timeout for the HTTP socket operation
            client.connect((host, port))
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
            client.send(request.encode())
            response = client.recv(4096)
            print(f"Received Response from Port {port}:\n{response.decode('utf-8')}")  # Print received response
            if b"html" in response:
                print(f"[+] {port}/tcp {protocol} [Open]")
            client.close()

        s.close()
    except (ConnectionRefusedError, socket.timeout):
        print(f"[-] {port}/tcp {protocol} [Closed]")

if __name__ == "__main__":
    target = input("Enter Target IP: ")
    print("[-] Start Port scanning on", target)

    ports_to_scan = [21, 80]  # Add more ports as needed
    for port in ports_to_scan:
        scan_port(target, port, "FTP" if port == 21 else "HTTP")


from sys import argv
from socket import *

server_ip = argv[1]
server_port = int(argv[2])

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((server_ip, server_port))

expected_seq = 0
file = None

print("waiting...")

while True:
    try:
        data, addr = sock.recvfrom(65507) 

        try:
            header, content = data.split(b":", 1) 
            seq_num = int(header.decode())
        except ValueError:
            continue  

        if seq_num < expected_seq:
            # Duplicated packet
            sock.sendto(f"ACK{seq_num}".encode(), addr)
            continue

        if seq_num == expected_seq:
            if file is None:
                file = open(content.decode(), "wb") 
                print("File created!")
            elif content == b"EOF":
                print("File transfer completed.")
                file.close()
                sock.sendto(f"ACK{seq_num}".encode(), addr)
                break
            else:
                file.write(content)  

            sock.sendto(f"ACK{seq_num}".encode(), addr)
            expected_seq += 1
    except KeyboardInterrupt:
        raise SystemExit

sock.close()
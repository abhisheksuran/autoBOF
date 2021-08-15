# autoBOF (BufferOverFlow)

## **** Under Development ****

## Description:
This repo contains some "Just working" scripts for buffer over Flows and exception handling is not implemented for inputs and other stuff.

1. autoBOF.py : Tried to provide some kind of automation for BufferOverFlow From fuzzing to the writing EIP with the jump pointer. U need to change IP, PORT, Prefix. At the state of finding bad characters, it expects only one bad character formated as "\x00".
2. finding_bad_char.py and find_badchar_auto.py : These two do same thing i.e finding bad characters while taking one bad character as input starting with "\x00". It automatically generates character list without the bad character.
3. exploit.py : To get a reverse shell by exploiting BOF.

You may try autoBOF.py or any other script.
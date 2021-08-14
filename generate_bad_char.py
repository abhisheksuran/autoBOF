# chars = ""
# for x in range(1, 256):
#      c = "\\x" + "{:02x}".format(x)
#      chars += c
#
#
# print(chars)
#
# char = []
# for x in range(1, 256):
#      cs = "{:02x}".format(x)
#      char.append(cs)
#
#
# print(char)
badchars = [r"\x00"]

badc = str(input("badchar"))
badchars.append(badc)
print(badchars)
#badchars = [r"\x00", r"\x07"]
chars = ""
for x in range(0, 256):
     c = "\\x" + "{:02x}".format(x)
     #print(c)
     #print(badchar)

     if str(c) not in badchars:
               chars += c
#chars = bytes(chars, "latin-1")
print(chars)

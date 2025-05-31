#!/usr/bin/python3

import sys

def main():
    code = sys.argv[1]
    decrypted = ""
    for i in range(len(code)):
        decrypted += chr(ord(code[i]) - i)
    print(decrypted) 

if __name__ == "__main__":
    main()
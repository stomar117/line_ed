#!/usr/bin/env python3.9

from reader import read

valid_commands = [
    "use", 
    "show", 
    "set", 
    "help", 
    "exit", 
    "back", 
    "clear", 
    "run", 
    "about", 
    "list", 
    "banner", 
    "alias", 
    "unalias", 
    "unset"
]

reader = read(valid_commands)
# reader = read()
try:
    history_buff: list = []
    while True:
        command = reader("\[test_prompt] ?>")
        if command == "exit":
            break
        elif command == "clear":
            print(chr(27)+'2[j')
            print('\033c')
            print('\x1bc')
        print(command)
except KeyboardInterrupt: print();pass
except EOFError: print();pass
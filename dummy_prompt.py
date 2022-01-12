#!/usr/bin/env python3.9

from reader import Reader

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

reader = Reader(valid_commands)
try:
    while True:
        command = reader.read("\[test_prompt] ?>")
        if command == "exit":
            break
except KeyboardInterrupt: print();pass
except EOFError: print();pass
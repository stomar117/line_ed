from .getch import Getch
from platform import platform

class getkey:
    '''
    Returns Keypress names depending on what key is returned by `Getch`.

    The Keycodes are:
    
        - RETURN  --> Returned when 'Enter' Key is pressed
        - UPKY    --> Returned when 'Up Arrow' key is pressed
        - DWKY    --> Returned when 'Down Arrow' key is pressed
        - RTKY    --> Returned when 'Right Arrow' key is pressed
        - LTKY    --> Returned when 'Left Arrow' key is pressed
        - DEL     --> Returned when 'Delete' key is pressed
        - BACK    --> Returned when 'Backspace' key is pressed
        - HOME    --> Returned when 'Home' key is pressed
        - END     --> Returned when 'End' key is pressed
        - C-{KEY} --> Returned when 'Control+Some Key' key is pressed
        - TAB     --> Returned when 'Tab' key is pressed
        - PGUP    --> Returned when 'Page Up' key is pressed
        - PGDW    --> Returned when 'Page Down' key is pressed
        - INS     --> Returned when 'Insert' key is pressed

    '''
    def __init__(self):
        pass

    def __call__(self):
        if 'Windows' in platform():
            return self._getkey_win()
        else:
            return self._getkey_unix()

    def _getkey_unix(self) -> str:
        key = Getch()()
        if key == '\r': return 'RETURN'
        if ord(key) == 27:
            newkey = Getch()()
            if ord(newkey) == 91:
                newkey = Getch()()
                if newkey == 'A': return 'UPKY'
                elif newkey == 'B': return 'DWKY'
                elif newkey == 'C': return 'RTKY'
                elif newkey == 'D': return 'LTKY'
                elif ord(newkey) == 72: return 'HOME'
                elif ord(newkey) == 70: return 'END'
                elif ord(newkey) == 51:
                    newkey = Getch()()
                    if ord(newkey) == 126: return 'DEL'
                elif ord(newkey) == 53:
                    newkey = Getch()()
                    if ord(newkey) == 126: return 'PGUP'
                elif ord(newkey) == 54:
                    newkey = Getch()()
                    if ord(newkey) == 126: return 'PGDW'
                elif ord(newkey) == 50:
                    newkey = Getch()()
                    if ord(newkey) == 126: return 'INS'
        elif ord(key) == 127: return 'BACK'
        elif ord(key) == 8: return 'C-BACK'
        elif ord(key) == 9: return 'TAB'
        if key.isprintable() and len(key) == 1:
            return key
        else:
            if chr(ord(key)+64).isalpha:
                return f'C-{chr(ord(key)+64)}'
            else: ord(key)

    def _getkey_win(self) -> str:
        key = Getch()()
        try:
            keypress = key.decode()
            if keypress == '\r': return 'RETURN'
            elif ord(keypress) == 8: return 'BACK'
            elif ord(keypress) == 127: return 'C-BACK'
            elif ord(keypress) == 9: return 'TAB'
            if keypress.isprintable() and len(keypress) == 1:
                return keypress
            else:
                if chr(ord(keypress)+64).isalpha:
                    return f'C-{chr(ord(keypress)+64)}'
        except UnicodeDecodeError:
            if key == b'\xe0':
                newkey = Getch()()
                if newkey.decode() == 'H': return 'UPKY'
                elif newkey.decode() == 'P': return 'DWKY'
                elif newkey.decode() == 'K': return 'LTKY'
                elif newkey.decode() == 'M': return 'RTKY'
                elif newkey.decode() == 'G': return 'HOME'
                elif newkey.decode() == 'O': return 'END'
                elif newkey.decode() == 'S': return 'DEL'
                else: return newkey.decode()
            else: return str(key)
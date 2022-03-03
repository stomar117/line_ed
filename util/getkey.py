from .getch import Getch
from platform import platform

class getkey:
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
        # if ord(key) == 4: return 'EOF'
        # if ord(key) == 3: return 'KBDINT'
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
        elif ord(key) == 127: return 'BACK'
        elif ord(key) == 8: return 'C-BACK'
        elif ord(key) == 9: return 'TAB'
        if key.isprintable() and len(key) == 1:
            return key
        else:
            if chr(ord(key)+64).isalpha:
                return f'C-{chr(ord(key)+64)}'
            else: return ''

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
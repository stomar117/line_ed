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
        if key == '\r': return 'EOL'
        if ord(key) == 4: return 'EOF'
        if ord(key) == 3: return 'KBDINT'
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
        elif ord(key) == 8: return 'C-BCK'
        elif ord(key) == 9: return 'TAB'
        if key.isprintable(): return key
        else: return ''

    def _getkey_win(self) -> str:
        key = Getch()()
        key.decode()
        return key
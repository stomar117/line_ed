from rich.console import Console
from sys import stdout
Console = Console()

def args(value: list, pos: int) -> str:
    try: return str(value[int(pos)])
    except Exception: return ''
from rich import traceback

traceback.install()

class Splitters:
    @staticmethod
    def bracket(string: str, bropen: str = '('):
        openbr: str = '({[<'
        closebr: str = ')}]>'
        if bropen in openbr: brclose = closebr[openbr.find(bropen)]
        else:
            print("Not a valid bracket...")
            return None
        str_container: list = []
        form_string: str = ''
        check: int = 0
        nbuff: int = 0
        for ch in string:
            if check == 1: form_string+=ch
            if ch == bropen:
                check = 1
                nbuff+=1
            if ch == brclose:
                nbuff-=1
                if nbuff == 0: check = 0
                if nbuff < 0:
                    print("Extra closing bracket found. Qutting...")
                    check = 1
                    break
            if check == 0:
                if form_string:
                    uneeded = list(form_string)
                    uneeded.pop()
                    form_string=''.join(uneeded)
                    del(uneeded)
                    str_container.append(form_string)
                    form_string = ''
        if check == 0: return str_container
        else:
            if nbuff >= 0: print("Extra opening bracket found. Quitting...")
            return None

    @staticmethod
    def dbreaker(string: str, delimiter: str = ' ') -> list:
        if delimiter.isalnum(): raise ValueError('delimitter cannot be an alpha-numeric character')
        if delimiter not in string: return [string]
        form_string: str = ''
        str_container: list = []
        check: int = 0
        for ch in string:
            if ch == '\'':
                if check == 2: pass
                elif check == 1: check = 0
                elif check == 0: check = 1
            if ch == '"':
                if check == 2: check = 0
                elif check == 1: pass
                elif check == 0: check = 2
            if ch == delimiter and check == 0: pass
            else: form_string+=ch
            if check == 0:
                if ch == delimiter:
                    str_container.append(form_string)
                    form_string=''
        if form_string:
            str_container.append(form_string)
        return str_container

    @staticmethod
    def quote(string: str, delimiter: str = ' ') -> list:
        if delimiter.isalnum(): raise ValueError('delimiter cannot be an alpha-numeric character')
        form_string: str = ''
        str_container: list = []
        quote_string: str = ''
        check: int = 0
        previous_state: int = 0
        for ch in string:
            previous_state = check
            if ch == '\'':
                if check == 2: pass
                elif check == 1:
                    quote_string+=ch
                    check = 0
                elif check == 0: check = 1
            if ch == '"':
                if check == 2:
                    quote_string+=ch
                    check = 0
                elif check == 1: pass
                elif check == 0: check = 2
            if check == 0:
                if previous_state != check:
                    str_container.append(quote_string)
                    quote_string = ''
                elif ch != delimiter and previous_state == check: form_string+=ch
                else:
                    if form_string:
                        str_container.append(form_string)
                        form_string=''
            else:
                if form_string: str_container.append(form_string); form_string=''
                # if check == 2 and ch == '"': pass
                # elif check == 1 and ch == '\'': pass
                else: quote_string+=ch
        if form_string: str_container.append(form_string)
        if quote_string: str_container.append(quote_string)
        return str_container

testlist: list = [ "clear", "use", "set", "exit", "prompt" ]

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class Reader:
    def __init__(self, valid_cmd_list: list, _history_buff: list = [])-> None:
        self.valid_cmd_list: list = valid_cmd_list
        self.history_buff: list = _history_buff
    def _prettify(self, string: str) -> str:
        splitted: list[str] = Splitters.quote(string)
        for idx, data in enumerate(splitted):
            # print()
            # print(data)
            # print()
            if idx == 0 and not ('"' in args(splitted, 0) or '\'' in args(splitted, 0)):
                # print(data)
                if args(splitted, 0) in self.valid_cmd_list:
                    splitted[0] = "[green]"+splitted[0]+"[/]"
                else:
                    splitted[0] = "[red]"+splitted[0]+"[/]"
            else:
                if data.startswith('-') and " " not in data:
                    splitted[idx] = "[blue]"+splitted[idx]+"[/]"
                if data.startswith('"'):
                    if data.endswith('"'):
                        splitted[idx] = "[bold yellow]"+splitted[idx]+"[/]"
                    else:
                        splitted[idx] = "[bold red]"+splitted[idx]+"[/]"
        else: pass
        #print(f'\n{splitted}')
        return ' '.join(splitted)
    
    def read(self, prompt: str = ">") -> str:
        req_line_buff_len: int = 0
        getch = _Getch()
        string: str = ''
        char: str = ''
        current: int = len(self.history_buff)-1
        while True:
            stdout.write('\033[2K\033[1G')
            # self._prettify(string)
            Console.print(f'\r{prompt} {self._prettify(string)}{" " if args(string, -1) == " " else ""}', end="")
            char = getch()
            # print(ord(char))
            if char == '\r':
                self.history_buff.append(string)
                break
            if ord(char) == 4: raise EOFError()
            if ord(char) == 3: raise KeyboardInterrupt()
            if ord(char) == 127:
                req_line_buff_len = len(string)
                try:
                    string_break = list(string)
                    string_break.pop()
                    string=''.join(string_break)
                    del string_break
                except IndexError:
                    string=''
                    pass
                finally:
                    continue
            if char.isprintable():
                string+=char
        print()
        return string
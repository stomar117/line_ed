from rich import console, traceback
from platform import platform
import _config as config
Console = console.Console()

def args(value: list, pos: int) -> str:
    try: return str(value[int(pos)])
    except Exception: return ''

traceback.install()

class Splitters:
    @staticmethod
    def bracket(string: str, bropen: str = '('):
        openbr: str = '({[<'
        closebr: str = ')}]>'
        if bropen in openbr: brclose = closebr[openbr.find(bropen)]
        else:
            # print("Not a valid bracket...")
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
                    # print("Extra closing bracket found. Qutting...")
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
            # if nbuff >= 0: print("Extra opening bracket found. Quitting...")
            return []

    @staticmethod
    def quote(string: str, delimiter: str = ' ') -> list:
        if delimiter.isalnum(): raise ValueError('delimiter cannot be an alpha-numeric character')
        form_string: str = ''
        str_container: list[str] = []
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
                elif check == 0:
                    quote_string+=ch
                    check = 1
            if ch == '"':
                if check == 1: pass
                elif check == 2:
                    quote_string+=ch
                    check = 0
                elif check == 0:
                    quote_string+=ch
                    check = 2
            if check == 0:
                if previous_state != check:
                    str_container.append(quote_string)
                    quote_string = ''
                elif ch != delimiter and previous_state == check: form_string+=ch
                else:
                    # if form_string:
                        str_container.append(form_string+ch)
                        form_string=''
            else:
                if form_string: str_container.append(form_string); form_string=''
                # if check == 2 and ch == '"': pass
                # elif check == 1 and ch == '\'': pass
                else:
                    if len(quote_string.strip()) == 1:
                        if ch == '\'' and quote_string == '\'': pass
                        elif ch == '"' and quote_string == '"': pass
                        else: quote_string+=ch

                    else: quote_string+=ch
        if form_string: str_container.append(form_string)
        if quote_string: str_container.append(quote_string)
        return str_container

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
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
    
    def _prettify(self, string: str):
        for x in '({[<':
            if x in string:
                for bracketed in Splitters.bracket(string):
                    string=string.replace(bracketed, f"[{config.bracketed}]"+bracketed+"[/]")
        splitted: list[str] = Splitters.quote(string)
        splitted_dup = splitted.copy()
        check = 0
        for idx, data in enumerate(splitted_dup):
            if data.strip().startswith('#'):
                splitted[idx]=f"[{config.comment}]"+splitted_dup[idx]+"[/]"
                for x in range(idx, len(splitted_dup)-1):
                    splitted[x]=f"[{config.comment}]"+splitted_dup[x]+"[/]"
                break
            if check == 0:
                if data.strip():
                    if data.strip() in self.valid_cmd_list:
                        splitted[idx] = f"[{config.valid_command}]"+data+"[/]"
                        check = 1
                    else:
                        splitted[idx] = f"[{config.invalid_command}]"+data+"[/]"
                        check = 1
            else:
                if data.strip().startswith('-'):
                    splitted[idx] = f"[{config.flags}]"+data+"[/]"
                elif data.strip().startswith('\''):
                    if data.strip().endswith('\'') and len(data.strip()) > 1:
                        splitted[idx] = f"[{config.quoted_string_complete}]"+data+"[/]"
                    else:
                        splitted[idx] = f"[{config.quoted_string_incomplete}]"+data+"[/]"

                elif data.strip().startswith('"'):
                    if data.strip().endswith('"') and len(data.strip()) > 1:
                        splitted[idx] = f"[{config.quoted_string_complete}]"+data+"[/]"
                    else:
                        splitted[idx] = f"[{config.quoted_string_incomplete}]"+data+"[/]"

        return ''.join(splitted)
    
    def read(self, prompt: str = '>') -> str:
        if 'Windows' in platform(): return self._read_windows(prompt)
        else: return self._read_unix(prompt)
    
    def _read_unix(self, prompt) -> str:
        getch = _Getch()
        string_bc: str = ''
        string_ac: str = ''
        char: str = ''
        current: int = len(self.history_buff)-1
        temp_string_buff=''
        while True:
            string = string_bc+string_ac
            print('\033[2K\033[1G', end='')
            # self._prettify(string)
            Console.print(f'\r{prompt} {self._prettify(string_bc+string_ac)}', end="\r")
            Console.print(f'\r{prompt} {self._prettify(string_bc)}', end="")
            char = getch()
            # print(ord(char))
            if char == '\r':
                self.history_buff.append(string)
                break
            if ord(char) == 4:
                print('^D')
                raise EOFError()
            if ord(char) == 3:
                if string_ac+string_bc:
                    string_ac=''
                    string_bc=''
                    print('^C')
                else:
                    raise KeyboardInterrupt()
            if ord(char) == 27:
                initializer = getch()
                if ord(initializer) == 91:
                    direction = getch()
                    if direction == 'A':
                        #UP
                        if string and not temp_string_buff: temp_string_buff = string
                        if current >= 0 and current < len(self.history_buff):
                            string_bc=self.history_buff[current]
                            current-=1
                        else:
                            if temp_string_buff:
                                string_bc = temp_string_buff
                                temp_string_buff = ''
                                current=len(self.history_buff)-1
                            else:
                                string_bc = args(string, -1)
                                current = len(self.history_buff)-1
                        string_ac=''
                    elif direction == 'B':
                        ## DOWN 
                        if current < len(self.history_buff):
                            current+=1
                            string_bc=args(self.history_buff, current)

                        else:
                            if temp_string_buff:
                                string_bc=temp_string_buff
                                temp_string_buff=''
                            else:
                                string_bc=''
                            current=len(self.history_buff)-1
                        string_ac=''
                    elif direction == 'C':
                        ## RIGHT
                        if string_ac:
                            string_bc+=string_ac[0]
                            if len(string_ac) > 1:
                                string_ac=string_ac[1::]
                            else:
                                string_ac=''
                        # print('RT')
                    elif direction == 'D':
                        ## LEFT
                        if string_bc:
                            temp_char = string_bc[-1]
                            string_bc=string_bc[:-1:]
                            temp_char+=string_ac
                            string_ac=temp_char
                            del temp_char

                    elif ord(direction) == 72:
                        ## HOME
                        string_ac=string_bc+string_ac
                        string_bc=''

                    elif ord(direction) == 70:
                        string_bc+=string_ac
                        string_ac=''

                    elif ord(direction) == 51:
                        new_unnamed_identifier = getch()
                        if ord(new_unnamed_identifier) == 126:
                            if len(string_ac) > 1:
                                string_ac=string_ac[1::]
                            else:
                                string_ac=''
            if ord(char) == 127:
                try:
                    string_bc = string_bc[:-1:]
                except IndexError:
                    string_bc=''
                    pass
                finally:
                    continue
            if ord(char) == 8:
                if string_bc:
                    strlist: list = string.split(' ')
                    if strlist[-1]:
                        strlist.pop()
                        string_bc=' '.join(strlist)
                    else:
                        for x in range(len(strlist)-1,-1, -1):
                            if strlist[x]:
                                strlist.pop()
                                break
                            else:
                                strlist.pop()
                        
                        string_bc=' '.join(strlist)
                    del strlist
                continue

            if len(str(char)) == 1 and str(char).isprintable():
                string_bc+=char
        string = string_bc+string_ac
        print()
        return string
    
    def _read_windows(self, prompt) -> str:
        getch = _Getch()
        string: str = ''
        current = len(self.history_buff)-1
        temp_string_buff: str = ''
        while True:
            last_buff: str = args(self.history_buff, -1)
            print('\033[2K\033[1G', end='')
            Console.print(f'\r{prompt} {self._prettify(string)}', end="")
            b_char = getch()
            try:
                char = bytes.decode(b_char, 'utf-8')
            except UnicodeDecodeError:
                if b_char == b'\xe0':
                    # print('directional_initiator')
                    direction = bytes.decode(getch(), 'utf-8')
                    # print(direction)
                    if direction == 'H':
                        ## UP
                        if string and not temp_string_buff: temp_string_buff = string
                        if current >= 0 and current < len(self.history_buff):
                            string=self.history_buff[current]
                            current-=1
                        else:
                            if temp_string_buff:
                                string = temp_string_buff
                                temp_string_buff = ''
                                current=len(self.history_buff)-1
                            else:
                                string = last_buff
                                current = len(self.history_buff)-1
                    if direction == 'P':
                        ## DOWN 
                        if current < len(self.history_buff):
                            current+=1
                            string=args(self.history_buff, current)

                        else:
                            if temp_string_buff:
                                string=temp_string_buff
                                temp_string_buff=''
                            else:
                                string=''
                            current=len(self.history_buff)-1
                    if direction == 'K': pass #print('LT')
                    if direction == 'M': pass #print('RT')
                else: print(b_char)
                continue
            if char == '\r':
                if args(self.history_buff, -1) != string:
                    self.history_buff.append(string)
                else:
                    pass
                break
            if ord(char) == 8:
                try:
                    string = string[:-1:]
                except IndexError:
                    string = ''
                    continue
            if ord(char) == 4: print('^D');raise EOFError
            if ord(char) == 3:
                if string:
                    print('^C')
                    string = ''
                else: raise KeyboardInterrupt
            # print(ord(char))
            if char.isprintable(): string+=char
        print()
        print(self.history_buff)
        return string
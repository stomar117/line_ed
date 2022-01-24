from rich import console, traceback
from platform import platform
from os import path
import _config as config
from util.splitters import Splitters
from util.getch import Getch
Console = console.Console()

def args(value: list, pos: int) -> str:
    try: return str(value[int(pos)])
    except Exception: return ''

def isfloat(string: str)->bool:
    ssplit = string.split('.')
    length: int = len(ssplit)
    FloatList: list = []
    if 0 < length <= 2:
        for x in ssplit:
            FloatList.append(x.isdecimal())
        if False in FloatList: return False
        else: return True
    else: return False

traceback.install()

class Reader:
    def __init__(self, valid_cmd_list: list, _history_buff: list = [])-> None:
        self.valid_cmd_list: list = valid_cmd_list
        self.history_buff: list = _history_buff

    def _paint_word(self, color: str, string: str) -> str:
        strsplit: list[str] = string.split(' ')
        strsplit[0]=f'[{color}]'+strsplit[0]+'[/]'
        string=' '.join(strsplit)
        del strsplit
        return string
    
    def _prettify(self, string: str) -> str:
        for x in '({<':
            if x in string:
                for bracketed in Splitters.bracket(string, bropen=x):
                    string=string.replace(bracketed, f"[{config.bracketed}]"+bracketed+"[/]")
        spilt_from_scln: list[str] = Splitters.dbreaker(string, delimiter=';')
        for index, string in enumerate(spilt_from_scln):
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
                            # splitted[idx] = f"[{config.valid_command}]"+data+"[/]"
                            splitted[idx] = self._paint_word(config.valid_command, data)
                            check = 1
                        else:
                            # splitted[idx] = f"[{config.invalid_command}]"+data+"[/]"
                            splitted[idx] = self._paint_word(config.invalid_command, data)
                            check = 1
                else:
                    if data.strip().startswith('-'):
                        splitted[idx] = self._paint_word(config.flags, data)
                    elif data.strip().startswith('\''):
                        if data.strip().endswith('\'') and len(data.strip()) > 1:
                            splitted[idx] = self._paint_word(config.quoted_string_complete, data)
                        else:
                            splitted[idx] = self._paint_word(config.quoted_string_incomplete, data)

                    elif data.strip().startswith('"'):
                        if data.strip().endswith('"') and len(data.strip()) > 1:
                            splitted[idx] = self._paint_word(config.quoted_string_complete, data)
                        else:
                            splitted[idx] = self._paint_word(config.quoted_string_incomplete, data)
                
                    elif path.exists(data.strip()):
                        splitted[idx] = self._paint_word(config.path_exists, data)
                
                    elif isfloat(data.strip()):
                        splitted[idx] = self._paint_word(config.integer, data)
            spilt_from_scln[index] = ''.join(splitted)
        return ''.join(spilt_from_scln)
    
    def _pretty_print(self, prompt: str, string_a: str, string_b: str):
        print('\033[2K\033[1G', end='')
        if '[' in (string_a+string_b):
            print(f'{prompt} {string_a+string_b}', end='\r')
            print(f'\r{prompt} {string_a}', end='')
        else:
            Console.print(f'{prompt} {self._prettify(string_a+string_b)}', end='\r')
            Console.print(f'{prompt} {self._prettify(string_a)}', end='')

    def read(self, prompt: str = '>') -> str:
        if 'Windows' in platform(): return self._read_windows(prompt)
        else: return self._read_unix(prompt)
    
    def _read_unix(self, prompt) -> str:
        getch = Getch()
        string_bc: str = ''
        string_ac: str = ''
        char: str = ''
        current: int = len(self.history_buff)-1
        temp_string_buff=''
        while True:
            string = string_bc+string_ac
            # self._prettify(string)
            self._pretty_print(prompt, string_bc, string_ac)
            char = getch()
            # print(ord(char))
            if char == '\r':
                self.history_buff.append(string)
                break
            if ord(char) == 4:
                if string_ac:
                    if len(string_ac) > 1:
                        string_ac=string_ac[1::]
                    else:
                        string_ac=''
                elif string_bc:
                    string_ac=string_bc=''
                else:
                    print('^D')
                    raise EOFError()
            if ord(char) == 3:
                if string_ac+string_bc:
                    string_ac=string_bc=''
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
                        ## END
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
        getch = Getch()
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
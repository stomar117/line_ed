from sys import stdout
from rich import console, traceback
from os import path, get_terminal_size
from math import ceil
import _config as config
from util.splitters import Splitters
Console = console.Console(highlight=False, soft_wrap=True,)

traceback.install()

class ReadUtils:
    def __init__(self, valid_cmd_list: list, _history_buff: list = [])-> None:
        self.valid_cmd_list: list = valid_cmd_list
        self.history_buff: list = _history_buff

    @staticmethod
    def args(value: list, pos: int) -> str:
        try: return str(value[int(pos)])
        except Exception: return ''

    @staticmethod
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

    def _paint_word(self, color: str, string: str) -> str:
        scln_ck: int = 0
        if string[-1] == ';':
            string=string[:-1:]
            scln_ck = 1
        if string[-1] == ' ':
            needed_string = string[:-1:]
            needed_string=f'[{color}]'+needed_string+('[/]' if not string.endswith('\\') or string.endswith('\\\\') else '\[/]')
            return needed_string+' '
        else:
            if scln_ck:
                return f'[{color}]'+self._prettify(string)+'[/];'
            return f'[{color}]'+string+('[/]' if not string.endswith('\\') or string.endswith('\\\\') else '\[/]')
    
    def _prettify(self, string: str) -> str:
        for x in '({<':
            if x in string:
                for bracketed in Splitters.bracket(string, bropen=x):
                    string=string.replace(bracketed, f"[{config.bracketed}]"+bracketed+"[/]")
        spilt_from_scln: list[str] = Splitters.dbreaker(string, delimiter=';')
        for index, string in enumerate(spilt_from_scln):
            # if self.args(string, -1) == ';':
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
                
                    elif self.isfloat(data.strip()):
                        splitted[idx] = self._paint_word(config.integer, data)
            spilt_from_scln[index] = ''.join(splitted)
        return ''.join(spilt_from_scln)
    
    def _pretty_print(self, prompt: str, string_a: str, string_b: str):
        term_col_size: float = float(get_terminal_size().columns)
        string_len: float = float(len(prompt+' '+string_a+string_b))
        line_count: int = ceil(string_len/term_col_size)
        if len((string_a+string_b)[int(term_col_size*line_count)::]) == 1 or ((string_a+string_b) if string_a+string_b else 'x')[-1] in '\t ':
            line_count=line_count-1
        print('\033[2K\033[1G', end='')
        for _ in range(line_count-1):
            print('\033[2K\033[1G', end='')
            print('\033[A', end='')
            stdout.flush()
        if '[' in (string_a+string_b):
            print(f'{prompt} {string_a+string_b}', end='\r')
            print(f'\r{prompt} {string_a}', end='')
        else:
            if string_b:
                Console.print(f'{prompt} {self._prettify(string_a+string_b)}', end='\r')
                Console.print(f'{prompt} {self._prettify(string_a)}', end='')
            else:
                Console.print(f'\r{prompt} {self._prettify(string_a)}', end='')
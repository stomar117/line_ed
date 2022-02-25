from util.readutil import ReadUtils
from util.getkey import getkey
from _config import bindings
from sys import stdin

class Read(ReadUtils):
    def __init__(self, valid_cmd_list: list[str]):
        super().__init__(valid_cmd_list)

    def read(self, prompt = '>') -> str:
        string_bc: str = ''
        string_ac: str = ''
        char: str = ''
        current: int = len(self.history_buff)-1
        temp_string_buff=''
        while True:
            string = string_bc+string_ac
            # self._prettify(string)
            self._pretty_print(prompt, string_bc, string_ac)
            keypress = getkey()()
            char = keypress if keypress.isprintable() else ''
            stdin.flush()
            if keypress == bindings.end_of_line:
                self.history_buff.append(string)
                break
            if keypress == bindings.end_of_file:
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
            if keypress == bindings.keyboard_interrupt:
                if string_ac+string_bc:
                    string_ac=string_bc=''
                    print('^C')
                else:
                    raise KeyboardInterrupt()

            if keypress == bindings.history_navigate_up:
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
                        string_bc = self.args(string, -1)
                        current = len(self.history_buff)-1
                string_ac=''
            elif keypress == bindings.history_navigate_down:
                ## DOWN 
                if current < len(self.history_buff):
                    current+=1
                    string_bc=self.args(self.history_buff, current)

                else:
                    if temp_string_buff:
                        string_bc=temp_string_buff
                        temp_string_buff=''
                    else:
                        string_bc=''
                    current=len(self.history_buff)-1
                string_ac=''
            elif keypress == bindings.line_navigate_right:
                ## RIGHT
                if string_ac:
                    string_bc+=string_ac[0]
                    if len(string_ac) > 1:
                        string_ac=string_ac[1::]
                    else:
                        string_ac=''

            elif keypress == bindings.line_navigate_left:
                ## LEFT
                if string_bc:
                    temp_char = string_bc[-1]
                    string_bc=string_bc[:-1:]
                    temp_char+=string_ac
                    string_ac=temp_char
                    del temp_char

            elif keypress == bindings.line_navigate_begin:
                ## HOME
                string_ac=string_bc+string_ac
                string_bc=''

            elif keypress == bindings.line_navigate_end:
                ## END
                string_bc+=string_ac
                string_ac=''

            if keypress == bindings.delete_on_current_position:
                if len(string_ac) > 1:
                    string_ac=string_ac[1::]
                else:
                    string_ac=''

            if keypress == bindings.delete_previous_position:
                try:
                    string_bc = string_bc[:-1:]
                except IndexError:
                    string_bc=''
                    pass
                finally:
                    continue
            if keypress == bindings.delete_previous_word:
                if string_bc:
                    strlist: list = string_bc.split(' ')
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

            if keypress == bindings.autocomplete:
                if string_bc:
                    if ' ' not in string_bc:
                        for word in self.valid_cmd_list:
                            if word.startswith(string_bc):
                                string_bc=word

            if len(str(char)) == 1 and str(char).isprintable():
                string_bc+=char
        string = string_bc+string_ac
        print()
        return string
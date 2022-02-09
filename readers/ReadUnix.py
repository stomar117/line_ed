from util.readutil import ReadUtils
from util.getch import Getch

class ReadUnix(ReadUtils):
    def __init__(self, valid_cmd_list):
        super().__init__(valid_cmd_list)

    def read(self, prompt = '>') -> str:
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
                                string_bc = self.args(string, -1)
                                current = len(self.history_buff)-1
                        string_ac=''
                    elif direction == 'B':
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
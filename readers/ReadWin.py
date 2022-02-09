from util.readutil import ReadUtils
from util.getch import Getch

class ReadWin(ReadUtils):
    def __init__(self, valid_cmd_list):
        super().__init__(valid_cmd_list)

    def read(self, prompt) -> str:
        getch = Getch()
        string: str = ''
        current = len(self.history_buff)-1
        temp_string_buff: str = ''
        while True:
            last_buff: str = self.args(self.history_buff, -1)
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
                            string=self.args(self.history_buff, current)

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
                if self.args(self.history_buff, -1) != string:
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
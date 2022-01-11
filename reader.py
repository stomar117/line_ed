import readchar
from rich.console import Console
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
                elif check == 1: check = 0
                elif check == 0: check = 1
            if ch == '"':
                if check == 2: check = 0
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
                if check == 2 and ch == '"': pass
                elif check == 1 and ch == '\'': pass
                else: quote_string+=ch
        if form_string: str_container.append(form_string)
        return str_container

testlist: list = [ "clear", "use", "set", "exit", "prompt" ]

string = ''
char = ''
print_string = ''
check = 0
while True:
    string+=char
    try:
        if char and char != ' ':
            nuisance = Splitters.quote(string)
            if args(nuisance, 0) in testlist:
                nuisance[0] = '[green]'+nuisance[0]+"[/]"
                print_string = f'{" ".join(nuisance)}|'
            else:
                nuisance[0] = '[red]'+nuisance[0]+'[/]'
                print_string = f'{" ".join(nuisance)}|'
        elif check != 0 and char != ' ':
            if args(Splitters.quote(string), 0):
                test = Splitters.quote(string)
                test[0] = "[green]" if test[0] in testlist else "[red]"+test[0]+"[/]"
                print_string = " ".join(test)+"| "
        elif char == " ":
            print(string+' |',end=' \r')
        Console.print(print_string, end="\r")
    except:
        pass
    char = readchar.readchar_linux.readchar()
    check = 1
    #print(len(string))
    if char == '\r': break
    if ord(char) == 127:
        char=''
        print(" "*len(string), end='\r')
        try:
            string = list(string)
            string.pop()
            string = ''.join(string)
            continue
        except IndexError:
            string = ''
            continue
print("\n"+string)

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
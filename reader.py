from readers.Reader import Read
class read:
    def __init__(self, cmd_list = None):
        self.cmd_list = cmd_list

    def __call__(self, prompt: str = '>'):
        return Read(self.cmd_list).read(prompt)
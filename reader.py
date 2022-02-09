from platform import platform

from readers.ReadWin import ReadWin
from readers.ReadUnix import ReadUnix
class read:
    def __init__(self, cmd_list):
        self.cmd_list = cmd_list

    def __call__(self, prompt: str = '>'):
        if 'Windows' in platform():
            return ReadWin(self.cmd_list).read(prompt)
        else:
            return ReadUnix(self.cmd_list).read(prompt)
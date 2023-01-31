from datetime import datetime
from colorama import init
from time import sleep
from getpass import getuser

import os

init(True)
class Console:
    RED = "\u001b[1;91m"
    RESET = "\u001b[0m"
    CYAN = "\u001b[1;96m"
    PURPLE = "\u001b[1;95m"
    GREEN = "\u001b[1;92m"
    WHITE = "\u001b[1;97m"
    BLUE = "\u001b[1;94m"
    __CMDLINE = f'{GREEN}Gryphon@{getuser()}{WHITE}:{BLUE}~{os.getcwd().split(getuser())[1]}{WHITE}${RESET} '
    BANNER = f"""{CYAN}
\t\t                        ______
\t\t             ______,---'__,---'
\t\t         _,-'---_---__,---'
\t\t  /_    (,  ---____',
\t\t /  ',,   `, ,-'
\t\t;/)   ,',,_/,'
\t\t| /\   ,.'//\\
\t\t`-` \ ,,'    `. 
\t\t     `',   ,-- `.
\t\t     '/ / |      `,         _
\t\t     //'',.\_    .\\      ,==>- 
\t\t  __//   __;_`-  \ `;.__,;'
\t\t((,--,) (((,------;  `--'
\t\t────────(GRYPHON)───────────
\t{PURPLE}>_ {RED}Helmsys  : https://github.com/Arif-Helmsys{CYAN}
    """

    @classmethod
    def display_links(cls,*printable:str):
        output = ""
        for out in printable:
            output += out + chr(32)
        print(
f"{cls.RED}[{cls.CYAN}+{cls.RED}] - {cls.PURPLE}{output}")
        sleep(0.2)

    @classmethod
    def display(cls,*obj:object):
        output = ""
        for out in obj:
            output += out + chr(32)
        print(output)

    @classmethod
    def warn_display(cls,printable:str):
        print(f"{cls.CYAN}[{cls.RED}*{cls.CYAN}] - {cls.GREEN}{printable}")
    
    @classmethod
    def err_display(cls,printable:str):
        print(f"{cls.CYAN}[{cls.RED}!{cls.CYAN}] - {cls.GREEN}{printable}")
    
    @classmethod
    def cmd_input(cls) -> str:
        return input(cls.__CMDLINE)
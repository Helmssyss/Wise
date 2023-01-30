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
{CYAN}\t\t  /_    (,  ---____',             {PURPLE}>_ {RED}Helmsys  : https://github.com/Arif-Helmsys
{CYAN}\t\t /  ',,   `, ,-'                  {PURPLE}>_ {RED}Coderx37 : https://github.com/fenrirsoftware
{CYAN}\t\t;/)   ,',,_/,'                    {PURPLE}>_ {RED}Nemesis  : https://github.com/nemes1spy{CYAN}
\t\t| /\   ,.'//\\
\t\t`-` \ ,,'    `. 
\t\t     `',   ,-- `.
\t\t     '/ / |      `,         _
\t\t     //'',.\_    .\\      ,==>- 
\t\t  __//   __;_`-  \ `;.__,;'
\t\t((,--,) (((,------;  `--'
\t\t────────(GRYPHON)───────────
    """

    @classmethod
    def display_links(cls,count,printable:str):
        print(
f"{cls.RED}├─[ {cls.CYAN}{datetime.now().strftime('%H:%M:%S')}{cls.RED} ] \
- [{cls.CYAN}{count:02d}{cls.CYAN}{cls.RED}] - {cls.PURPLE}{printable}")
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
        return input(Console.__CMDLINE)

# Console.cmd_input()
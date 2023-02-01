from datetime import datetime
from colorama import init
from time import sleep
from getpass import getuser
from rich.live import Live
from rich.table import Table, Column
from rich.box import SIMPLE_HEAVY

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
    BANNER = f"""{BLUE}
\t\t                       ,---.
\t\t                       /    |
\t\t                      /     |
\t\t                     /      |
\t\t                    /       |
\t\t               ___,'        |
\t\t             <  -'          :
\t\t              `-.__..--'``-,_\_
\t\t                 |o/ ` :,.)_`>
\t\t                :/ `     ||/)
\t\t                 (_.).__,-` |\\
\t\t                 /( `.``   `| :
\t\t                 \'`-.)  `  ; ;
\t\t                 | `       /-<
\t\t                 |     `  /   `.
\t\t ,-_-..____     /|  `    :__..-'\\
\t\t/,'-.__\\  ``-./ :`      ;       \\
\t\t`\ `\  `\\  \ :  (   `  /  ,   `. \\
\t\t  \` \   \\   |  | `   :  :     .\ \\
\t\t   \ `\_  ))  :  ;     |  |      ):
\t\t  (`-.-'\ ||  |\ \   ` ;  ;       |
\t\t   \-_   `;;._   ( `  /  /_       |
\t\t    `-.-.// ,'`-._\__/_,'         ;
\t\t       \:: :     /     `     ,   /  
\t\t        || |    (        ,' /   /   
\t\t        ||                ,'   /           
\t\t\t \{PURPLE} _      __(_)_______{CYAN}/{PURPLE} 
\t\t\t  | | /| / / / ___/ _ \\
\t\t\t  | |/ |/ / (__  )  __/
\t\t\t  |__/|__/_/____/\___/
\t\t    {BLUE}https://github.com/Arif-Helmsys
    """

    @classmethod
    def display_links(cls,*printable:str):
        output = ""
        for out in printable:
            output += out + chr(32)
        print(
f"{chr(32)*3}{cls.RED}[{cls.CYAN}+{cls.RED}]{cls.PURPLE}{output}")
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
    
    @classmethod
    def setTable(cls,*column,title):
        columns:list[Column] = []
        for c in column:
            columns.append(Column(c,justify="center",no_wrap=True))

        cls.table_ = Table(*columns,box=SIMPLE_HEAVY,title=title)

    @classmethod
    def table(cls,queue_):
        with Live(cls.table_):
            while not queue_.empty():
                try:
                    screen_name,location,follower_count = queue_.get()
                    if location == '':
                        location = '[bold red]*'
                    cls.table_.add_row("[bold red][[bold cyan]+[bold red]]",f"[bold magenta]{screen_name}",f"[bold magenta]{location}",f"[bold magenta]{follower_count}")
                    sleep(0.2)
                    queue_.task_done()
                except:
                    cls.table_.add_row(f"[bold red][[bold cyan]+[bold red]] [bold magenta]{queue_.get()}",end_section=True)
                    sleep(0.2)
                    queue_.task_done()

print(Console.BANNER)
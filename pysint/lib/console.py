from datetime import datetime
from colorama import init,Fore
from time import sleep

init(True)
class Console:
    RED = Fore.LIGHTRED_EX
    RESET = Fore.RESET
    CYAN = Fore.LIGHTCYAN_EX
    MAGENTA = Fore.LIGHTMAGENTA_EX
    BANNER = """
HOŞ GELDİN
    """.strip()

    @classmethod
    def display_links(cls,count,printable:str):
        print(
f"{cls.RED}[ {cls.CYAN}{datetime.now().strftime('%H:%M:%S')}{cls.RED} ] \
[{cls.CYAN}{count:02d}{cls.CYAN}{cls.RED}] - {cls.MAGENTA}{printable}")
        sleep(0.2)

    @classmethod
    def err_display(cls,printable:str):
        print(f"{cls.CYAN}[ {cls.RED}!{cls.CYAN} ] - {Fore.LIGHTGREEN_EX}{printable}")
    
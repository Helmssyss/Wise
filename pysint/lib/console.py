from datetime import datetime
from colorama import init
from time import sleep

init(True)
class Console:
    RED = "\u001b[1;91m"
    RESET = "\u001b[0m"
    CYAN = "\u001b[0;36m"
    PURPLE = "\u001b[1;95m"
    GREEN = "\u001b[0;32m"
    BANNER = """\n
GÜZEL BİR BANNER İÇİN HALA ZAMAN VAR
    """.strip()

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
    
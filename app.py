from argparse import ArgumentParser
from pysint import (Console,Search)
from os import name as os_name
from os import system


console = Console()
def argParse():
    argP:ArgumentParser = ArgumentParser(description='How to Using')
    argP.add_argument("-q","--query","--dork",type=str,nargs='*')
    argP.add_argument("-s","--social-media",action='store_true') # yalnızca özenle seçilen sosyal medya da arar
    argP.add_argument("-f","--filter",type=str,nargs='*',help="Özellikle belirtilen url adına işlem yapar")
    argP.add_argument("-px","--proxy",type=str,help="Proxy dosya yolu TxT formatında dosya gerekli.")
    return argP.parse_args()

def main():
    __arguments = argParse()
    if __arguments.query and __arguments.social_media:
        system('cls'if os_name == 'nt' else 'clear')
        console.BANNER
        with Search(query=__arguments.query,social_media=__arguments.social_media) as search:
            search.start()
            search.result()

    elif __arguments.query or __arguments.filter:
        system('cls'if os_name == 'nt' else 'clear')
        console.BANNER
        with Search(query=__arguments.query,filters=__arguments.filter) as search:
            search.start()
            search.result()
    else:
        console.warn_display(f"{console.CYAN}Başlamak için: {console.PURPLE}python app.py -h")

if __name__ == "__main__":
    main()
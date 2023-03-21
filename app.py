from wise import Search,Console,ProxyManager
from argparse import ArgumentParser


def argParse():
    argP:ArgumentParser = ArgumentParser(description='How to Using')
    argP.add_argument("-q","--query","--dork",type=str,nargs='*')
    argP.add_argument("-s","--social-media",action='store_true') # yalnızca özenle seçilen sosyal medya da arar
    argP.add_argument("-f","--filter",type=str,nargs='*',help="Özellikle belirtilen url adına işlem yapar")
    argP.add_argument("-px","--proxy",nargs='?')
    return argP.parse_args()

def mainPage():
    console = Console()
    args = argParse()
    if args.query:
        console.BANNER
        search = Search(query=args.query,filters=args.filter,social_media=args.social_media,proxy=args.proxy)
        search.start()
    else:
        console.print("To Started: [code]python .\\app.py -h[/code]")

mainPage()
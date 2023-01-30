from argparse import ArgumentParser
from pysint import Search,Console

class App:
    def __init__(self) -> None:
        self.engines = ["google","bing"]
    def __argParse(self):
        argP:ArgumentParser = ArgumentParser(description='How to Using')
        argP.add_argument("-q","--query","--dork",type=str,nargs='*')
        argP.add_argument("-s","--social-media",action='store_true') # yalnızca özenle seçilen sosyal medya da arar
        argP.add_argument("-e","--engine",type=str)
        argP.add_argument("-f","--filter",type=str,nargs='*',help="Özellikle belirtilen url adına işlem yapar")
        argP.add_argument("-px","--proxy",type=str,help="Proxy dosya yolu TxT formatında dosya gerekli.")
        return argP.parse_args()

    def run(self):
        __arguments = self.__argParse()
        if (__arguments.query):
            Console.display(Console.BANNER)
            search = Search( __arguments.query,__arguments.filter,__arguments.social_media) # __arguments.query,__arguments.filter
            search.getSearchedLinks()
        else:
            Console.display(f"\n{Console.CYAN}Başlamak için: {Console.PURPLE}python app.py -h")

if __name__ == "__main__":
    app:App = App()
    app.run()

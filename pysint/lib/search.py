from .const import *
from .proxies import proxies
from .console import Console
from bs4 import BeautifulSoup
from re import search as re_search
from urllib.parse import urlparse
from time import sleep
import threading
import queue
import typing
import requests

class Search:
    __threads:list[threading.Thread] = []
    __lock = threading.Lock()
    __que = queue.Queue()
    page:int = 11 # test amaçlı 10
    # flag
    def __init__(self,query:typing.Optional[str]=None,filter:typing.Optional[str]=None) -> None:
        self.__filter = filter
        self.__query = query
        if isinstance(filter,str):
            filter.lower()

    def __getCookie(self,main_url:str) -> dict:
        __result = requests.get(main_url,headers=HEADER)
        __cookies = __result.cookies.get_dict()
        return __cookies

    def __linkfilter(self,response:requests.Response,attr:dict,_filter:bool=False):
        soup = BeautifulSoup(response.content,"lxml")
        if _filter:
            print(_filter,self.__filter)
            for i in  soup.find_all("div",attrs=attr):
                try:
                    self.__lock.acquire()
                    link = i.a["href"]
                    match = re_search(r"\b{0}\b".format(self.__filter),link)
                    if match:
                        self.__que.put(match.string)
                except Exception as e:
                    continue
                finally:
                    self.__lock.release()

        else:
             for i in soup.find_all("div",attrs=attr):
                try:
                    self.__lock.acquire()
                    if i.a['href'].startswith("https"):
                        self.__que.put(i.a['href'])
                except Exception as e:
                    continue
                finally:
                    self.__lock.release()

    def __request(self,slot:int,_filter:bool=True):
        params = {
            "q" : self.__query,
            "start": slot
        }
        response = requests.get(GOOGLESEARCH,params=params,headers=HEADER,cookies=self.__getCookie(GOOGLEMAIN))
        soup = BeautifulSoup(response.content,"lxml")
        capctha = soup.find("form",attrs={"id":"captcha-form"})
        attr = {"class":"yuRUbf"}
        if capctha: # captcha yakalanırsa
            print("BING")
            params = {
                "q" : self.__query,
                "sp":'1',
                "first": slot
            }
            response = requests.get(BINGSEARCH,params=params,headers=HEADER,cookies=self.__getCookie(BINGMAIN))
            soup = BeautifulSoup(response.content,"lxml")
            attr = {"class":"b_title"}
            return self.__linkfilter(response,attr,_filter)

        if capctha == None: # captcha yakalanmazsa
            print("GOOGLE")
            if _filter: #filtre kullanılırsa
                return self.__linkfilter(response,attr,_filter)

            else: #filtre kullanılmazsa
                return self.__linkfilter(response,attr)

    def searchQuerySet(self,slot:int):
        if isinstance(self.__filter,str):
            return self.__request(slot=slot)

        else:
            return self.__request(slot=slot,_filter=False)

    def getSearchedLinks(self):
        for i in range(1, 11 if self.page == 1 else (self.page * 10) + 1 ,11):
            t = threading.Thread(target=self.searchQuerySet,args=(i,))
            t.start()
            self.__threads.append(t)

        for thread in self.__threads:
            thread.join()

        count = 0
        if self.__que.qsize() != 0:
            Console.display(f"{chr(32)*7}{Console.CYAN}TIME{chr(32)*6}COUNT{chr(32)*9}LINKS")
            while not self.__que.empty():
                count += 1
                Console.display_links(count,self.__que.get())
            Console.display(f"{Console.GREEN}|                            |")
            Console.display(f"{Console.GREEN}├───────({Console.CYAN}OSINT FINISHED{Console.GREEN})─────╯")
            Console.display(f"{Console.GREEN}|\n╰───────({Console.CYAN}ARATILAN{Console.GREEN})──[{Console.CYAN}{self.__query}{Console.GREEN}]")
        else:
            Console.warn_display("No Results\n")
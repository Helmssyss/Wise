from .const import *
from .proxies import proxies
from .console import Console
from bs4 import BeautifulSoup
from re import search as re_search
from urllib.parse import urlparse

import threading
import queue
import typing
import requests

class Search:
    __threads:list[threading.Thread] = []
    __lock = threading.Lock()
    __que = queue.Queue()
    page:int = 5 # test amaçlı 10
    def __init__(self,query:typing.Optional[str]=None,filter:typing.Optional[str]=None) -> None:
        print(Console.BANNER.strip())
        self.__filter = filter
        self.__query = query
        if isinstance(filter,str):
            filter.lower()

    def __getCookie(self) -> dict:
        __result = requests.get("https://www.google.com/",headers=HEADER)
        __cookies = __result.cookies.get_dict()
        return __cookies
    
    def __request(self,slot:int,_filter:bool=True):
        params = {
            "q" : self.__query,
            "start": slot
        }
        response = requests.get("https://www.google.com/search",params=params,headers=HEADER,cookies=self.__getCookie())
        soup = BeautifulSoup(response.content,"lxml")
        if _filter:
            for i in  soup.find_all("div",attrs={"class":"yuRUbf"}):
                self.__lock.acquire()
                link = i.a["href"]
                match = re_search(r"\b{0}\b".format(self.__filter),link)
                if match:
                    self.__que.put(match.string)
                self.__lock.release()

        else:
            for i in soup.find_all("div",{"class":"yuRUbf"}):
                self.__lock.acquire()
                self.__que.put(i.a['href'])
                self.__lock.release()

    def searchQuerySet(self,slot:int):
        if isinstance(self.__filter,str):
            self.__request(slot=slot)

        else:
            self.__request(slot=slot,_filter=False)

    def getSearchedLinks(self):
        for p in range(0, self.page*10 if self.page == 1 else (self.page) * 10, 10):
            t = threading.Thread(target=self.searchQuerySet,args=(p,),daemon=True)
            t.start()
            self.__threads.append(t)
        
        for thread in self.__threads:
            thread.join()

        count = 0
        if self.__que.qsize() != 0:
            while not self.__que.empty():
                count += 1
                Console.display_links(count,self.__que.get())
            print("\n")
        else:
            Console.err_display("No results\n")
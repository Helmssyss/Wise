from ..console import Console
from ..const import HEADER,userAgent,BINGSEARCH,GOOGLESEARCH,BINGMAIN
from ..social import Twitter,TikTok
from typing import Optional
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from re import search as re_search

import threading
import queue
import os
import time

safe = threading.Lock()
event = threading.Event()
console = Console()
queue_ = queue.Queue()


# spesific social media classes
twitter = Twitter(user_agent=userAgent())   # instagram ve youtube eklenecek
tiktok = TikTok()
# spesific social media classes

class MainSearch:
    def __init__(self,query:list[str],filters:list[str]=None,social_media:bool = False) -> None:
        self.__filter = filters
        self.__cookies = {} # private cookie
        self.__query = ""
        self.social_media = social_media
        self._page = 5 #protected page
        for q in query:
            self.__query += q + '+'
        self.__query = self.__query[:len(self.__query)-1]

        if isinstance(filters,list):
            self.__filter = [i.lower() for i in filters]

    @property
    def _isFoundCaptcha(self):
        with Session() as session:
            params = {"q" : "'","start": '1'}
            response = session.get("https://www.google.com/search",params=params,headers=HEADER)
            soup = BeautifulSoup(response.content,"lxml")
            captcha = soup.find("form",attrs={"id":"captcha-form"})
            if not captcha: # Captcha Yok
                return True

            else: # Captcha Var
                console.err_display("F_ck, Captcha!")
                return False

    def __setFilter(self,link:str,filter_:list=None):
        for i in filter_:
            match = re_search(r"\b{0}\b".format(i),link)
            if match:
                safe.acquire()
                queue_.put(match.string)
                safe.release()

    def _getCookie(self,base_url) -> dict:
        with Session() as session:
            __result = session.get(base_url,headers=HEADER)
            self.__cookies.update(__result.cookies.get_dict())
        return self.__cookies

    def _searchQuery(self,slot,search_url:str=GOOGLESEARCH,link_attr:str="yuRUbf"):
        with Session() as session:
            params = {"q" : self.__query,"start": slot}
            response = session.get(search_url,params=params,headers=HEADER,cookies=self.__cookies,timeout=3)
            soup = BeautifulSoup(response.content,"lxml")
            event.wait()
            for i in  soup.find_all("div",attrs={"class":link_attr}):
                try:
                    link = i.a['href']
                    if "bing" not in urlparse(link).netloc or "books" not in urlparse(link).netloc:
                        if "/videos/search" not in link:
                            if self.__filter != None:
                                self.__setFilter(link,self.__filter)
                            else:
                                safe.acquire()
                                queue_.put(link)
                                safe.release()
                except:
                    print("link",link)

    def __social(self):
        twitter.username = self.__query.split('+')
        social_threads = []
        for i in range(10):
            t = threading.Thread(target=twitter.get,args=(i,queue_))
            t.start()
            social_threads.append(t)
        
        for t in social_threads:
            t.join()

    def _result(self):
        while not queue_.empty():
            console.display_links(queue_.get())
            time.sleep(0.2)
            queue_.task_done()

    def _start(self):
        if not self.social_media: # -s argümanı kullanılmazsa
            for p in range(0, self._page*10 if self._page == 1 else (self._page) * 10, 10):
                thread = threading.Thread(target=self._searchQuery,args=(p,))
                thread.start()

            console.progress_bar(threading.active_count())
            event.set()
            print("────────────────────────────────RESULT────────────────────────────────")
            time.sleep(0.2)
            self._result()

        else: # -s argümanı kullanılırsa
            self.__social()
            console.setTable("[red][[green]USER[red]]",
                             "[red][[green]LOCATION[red]]",
                             "[red][[green]FOLLOWERS[red]]",
                             title="[italic bold cyan]Twitter")
            console.table(queue_)
            # self._result()
        

class Search(MainSearch):
    def __init__(self, query: list[str], filters: list[str] = None, social_media: bool = False) -> None:
        self._page = 6
        super().__init__(query, filters, social_media)

    def __enter__(self):
        return self

    def __exit__(self,*args):
        del self

    def _getCookie(self) -> dict:
        return super()._getCookie(BINGMAIN)

    def result(self):
        return super()._result()

    def start(self):
        if self._isFoundCaptcha:
            print("google")
            return super()._start()

        else:
            print("bing")
            for p in range(1, 11 if self._page == 1 else (self._page * 10) + 1 ,11):
                thread = threading.Thread(target=self._searchQuery,args=(p,BINGSEARCH,"b_title"))
                thread.start()

            console.progress_bar(threading.active_count())
            event.set()
            time.sleep(0.2)
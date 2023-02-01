from .const import *
from .proxies import proxies
from .console import Console
from .twitter import Twitter
from ..exceptions import CaptchaError
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
    __lock:threading.Lock = threading.Lock()
    __que:queue.Queue = queue.Queue()
    __event:threading.Event = threading.Event()
    page:int = 11 # test amaçlı 10
    # flag
    def __init__(self,query:typing.Optional[list]=None,filter:typing.Optional[list]=None,social_media:typing.Optional[bool]=False):
        self.__filter = filter
        self.__query = ""
        self.__social_media = social_media
        self.__twitter = Twitter(requests)
        for q in query:
            self.__query += q+'+'
        self.__query = self.__query[:len(self.__query)-1]
        if isinstance(filter,list):
            self.__filter = [i.lower() for i in filter]

    def __getCookie(self,main_url:str) -> dict[str,str]:
        __result = requests.get(main_url,headers=HEADER)
        __cookies = __result.cookies.get_dict()
        return __cookies

    def __linkfilter(self,response:requests.Response,attr:dict,_filter:bool=False):
        soup = BeautifulSoup(response.content,"lxml")
        if _filter:
            for i in soup.find_all("div",attrs=attr):
                try:
                    for j in self.__filter:
                        link = i.a["href"]
                        match = re_search(r"\b{0}\b".format(j),link)
                        if match:
                            self.__que.put(match.string)
                except Exception as e:
                    continue

        else:
             for i in soup.find_all("div",attrs=attr):
                try:
                    if i.a['href'].startswith("https"):
                        if "books" not in urlparse(i.a['href']).netloc:
                            self.__que.put(i.a['href'])
                except Exception as e:
                    continue

    def __request(self,slot:int):
        try:
            self.__findCaptcha()
            # print("GOOGLE")
            self.__searchEngine(slot)

        except CaptchaError:
            self.__event.set()
            # print("BING")
            self.__searchEngine(slot,True)

    def searchQuerySet(self,slot:int):
        if isinstance(self.__filter,str):
            return self.__request(slot=slot)

        else:
            return self.__request(slot=slot)

    def getSearchedLinks(self):
        if not self.__social_media:
            for i in range(1, 11 if self.page == 1 else (self.page * 10) + 1 ,11):
                t = threading.Thread(target=self.searchQuerySet,args=(i,))
                t.start()
                self.__threads.append(t)

            for thread in self.__threads:
                thread.join()

            if self.__event.is_set():
                Console.warn_display("F_ck, Captcha!")
                sleep(1)
                Console.warn_display("Alternative Searched...")
                self.__event.clear()
                sleep(1)

            if self.__que.qsize() != 0:
                Console.warn_display("Searched Internet...")
                sleep(1)
                Console.warn_display(f"   {self.__que.qsize()} Link")
                Console.display("──"*30)
                while not self.__que.empty():
                    Console.display_links(f"\t{self.__que.get():<10}")
                    self.__que.task_done()
                    
                Console.display(f"\n{Console.GREEN}{Console.CYAN}Search has end{Console.GREEN}")
            else:
                Console.err_display("No Results")

        else:
            self.__threads.clear()
            for i in range(10):
                t = threading.Thread(target=self.social,args=(i,))
                t.start()
                self.__threads.append(t)

            for thread in self.__threads:
                thread.join()
            
            if self.__que.qsize() != 0:
                Console.setTable("[red][[cyan]STATE[red]]","[red][[green]USER[red]]","[red][[green]LOCATION[red]]","[red][[green]FOLLOWERS[red]]",title="[italic bold cyan]Twitter")
                Console.table(self.__que)

    def __searchEngine(self,slot:int,other_engine:bool=False):
        if not other_engine:
            #Google
            params = {
                "q" : self.__query,
                "start": slot
            }
            response = requests.get(GOOGLESEARCH,params=params,headers=HEADER,cookies=self.__getCookie(GOOGLEMAIN))
            attr = {"class":"yuRUbf"}
            return self.__linkfilter(response,attr,isinstance(self.__filter,list))
        else:
            try:
                #Bing
                params = {
                    "q" : self.__query,
                    "sp":'1',
                    "first": slot
                }
                response = requests.get(BINGSEARCH,params=params,headers=HEADER,cookies=self.__getCookie(BINGMAIN))
                attr = {"class":"b_title"}
                return self.__linkfilter(response,attr,isinstance(self.__filter,list))
            except requests.exceptions.ChunkedEncodingError:
                pass
    
    def __findCaptcha(self):
        params = {
            "q" : self.__query,
            "start": '1'
        }
        response = requests.get(GOOGLESEARCH,params=params,headers=HEADER,cookies=self.__getCookie(GOOGLEMAIN))
        soup = BeautifulSoup(response.content,"lxml")
        captcha = soup.find("form",attrs={"id":"captcha-form"})
        # captcha = True
        if captcha:
            raise CaptchaError()

    def social(self,num:int):
        try:
            searched = self.__twitter.getUser(self.__query.split('+'),userAgent())
            screen_name = searched["users"][num]["screen_name"]
            location = searched["users"][num]["location"]
            follower_count = self.__twitter.followerCount(screen_name)
            self.__que.put((screen_name,location,follower_count))
        except IndexError:
            pass
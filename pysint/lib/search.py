from .const import *
from .proxies import proxies
from .console import Console
from .twitter import Twitter
from ..exceptions import CaptchaError
from bs4 import BeautifulSoup
from re import search as re_search
from urllib.parse import urlparse
from time import sleep
from pandas import DataFrame

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
        self.__user_social_medias_searched:list[tuple] = []
        self.__twitter = Twitter(requests)
        for q in query:
            self.__query += q+'+'
        self.__query = self.__query[:len(self.__query)-1]
        print(self.__query)
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
                    self.__lock.acquire()
                    for j in self.__filter:
                        link = i.a["href"]
                        match = re_search(r"\b{0}\b".format(j),link)
                        if match:
                            print(_filter,j)
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
                        if "books" not in urlparse(i.a['href']).netloc:
                            self.__que.put(i.a['href'])
                except Exception as e:
                    continue
                finally:
                    self.__lock.release()

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
                sleep(2)

            if self.__que.qsize() != 0:
                while not self.__que.empty():
                    Console.display_links(self.__que.get())
                    self.__que.tast_done()
                    
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
                Console.display("screen_name\t","name\t","location\t")
                Console.display("──"*30)
                while not self.__que.empty():
                    screen_name,name,location = self.__que.get()
                    Console.display_links(f"{screen_name:<20}",f"{name:<20}",f"{location:<50}")

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
            #Bing
            params = {
                "q" : self.__query,
                "sp":'1',
                "first": slot
            }
            response = requests.get(BINGSEARCH,params=params,headers=HEADER,cookies=self.__getCookie(BINGMAIN))
            attr = {"class":"b_title"}
            return self.__linkfilter(response,attr,isinstance(self.__filter,list))
    
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
        for user in self.__query.split('+'):
            try:
                searched = self.__twitter.userSearch(user,userAgent())
                screen_name = searched["users"][num]["screen_name"]
                name = searched["users"][num]["name"]
                location = searched["users"][num]["location"]
                self.__que.put((screen_name,name,location))
            except:
                pass

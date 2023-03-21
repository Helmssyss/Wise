from .const import (HEADER,BINGMAIN,BINGSEARCH,GOOGLEMAIN,GOOGLESEARCH)
from .console import Console
from .social import Twitter,Instagram
from threading import (Lock,Event,Thread,active_count)
from queue import Queue
from requests import Session
from typing import Optional,Union
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import time
import re

class __MainSearch:
    def __init__(self,query:Optional[list[str]]=None,
        filters:Optional[list[str]]=None,
        social_media:Optional[bool]=False,
        proxy:str=None) -> None:
        self.proxy = proxy
        self.console = Console()
        self.safe = Lock()
        self.event = Event()
        self.queue = Queue()
        self.query = ""
        self.page = 5
        self.filter = filters
        self.social_media = social_media
        self.cookies = {}
        self.url_attr = {"google":"yuRUbf","bing":"b_title"}
        for q in query:
            self.query += q + ' '
        self.query = self.query[:len(self.query)-1]

    def getCookies(self,base_url):
            with Session() as session:
                return session.get(base_url,headers=HEADER).cookies.get_dict()

    def isFoundCaptcha(self) -> bool:
        with Session() as session:
            params = {"q" : "test","start": '1'}
            response = session.get("https://www.google.com",params=params,headers=HEADER)
            soup = BeautifulSoup(response.content,"lxml")
            captcha = soup.find("form",attrs={"id":"captcha-form"})
            # return False
            if captcha or captcha == None:
                return True # Captcha var
            else:
                return False # Captcha Yok 'False' test için 'True Yap'

    def urlParsed(self,url:str):
        return re.findall('://www.([\w\-\.]+)',url)

    def searchQuery(self,slot,search_url,attr):
        with Session() as session:
            params = {}
            cookie = {}
            if search_url == GOOGLESEARCH:
                params = {"q" : self.query,"start": slot}
                cookie = self.getCookies(GOOGLEMAIN)
            elif search_url == BINGSEARCH:
                params = {"q":self.query,"sp":"1","first":slot}
                cookie = self.getCookies(BINGMAIN)
                
            response = session.get(search_url,headers=HEADER,params=params,cookies=cookie)
            # print(response.url)
            soup = BeautifulSoup(response.content,"lxml")
            self.event.wait()
            for data in soup.find_all("div",attrs={"class":attr}):
                try:
                    if urlparse(data.a['href']) != ["bing.com"] or urlparse(data.a['href'])[0] != "books.google.com.tr":
                        if self.filter == None:
                            self.safe.acquire()
                            self.console.display_links(data.a['href'])
                            time.sleep(0.2)
                            self.safe.release()
                        else:
                            self.__filter(data.a['href'],self.filter)
                except Exception as e:
                    pass
                    # print(e,slot,search_url,attr)
    
    def __filter(self,data,filter_):
        for i in filter_:
            match = re.search(r"\b{0}\b".format(i),data)
            if match:
                self.console.display_links(match.string)
                time.sleep(0.2)

    def social_data(self):
        twitter = Twitter()
        instagram = Instagram(self.proxy)
        twitter.username = self.query.split('+')
        instagram.username = self.query.split('+')
        instagram.getCSRFtoken()
        social_threads = []

        for i in range(10):
            t = Thread(target=twitter.getUsers,args=(i,),daemon=True)
            t.start()
            social_threads.append(t)

        instagram.userSearch()
        # instagram.getUsers(1)
        for i in range(20):
            t = Thread(target=instagram.getUsers,args=(i,))
            t.start()

        self.console.print(f"\t\t [bold green][[red]*[bold green]] THREAD : [purple]{active_count() - 1}{chr(32)*(len(str(self.filter))+1)}[/purple][bold green][[red]*[bold green]] QUERY : [purple]{self.query.replace('+',' ')}[/purple]")
        self.console.print(f"\t\t [bold green][[red]*[bold green]] FILTER : [/bold green]{self.filter}  [bold green][[red]*[bold green]] SOCIAL-MEDIA : [purple]{self.social_media}[/purple]\n")
        self.console.progress_bar(active_count() - 1)
        for t in social_threads:
            t.join()

        self.console.setTable("[NAME]","[FOLLOWER]","[VERIFIED]",title="Twitter")
        self.console.table(twitter.result_data,link="https://twitter.com/")

        self.console.setTable("[NAME]","[FOLLOWER]","[VERIFIED]",title="Instagram")
        self.console.table(instagram.data,link="https://instagram.com/")


class Search(__MainSearch):
    def __init__(self, query: Optional[list[str]] = None, filters: Optional[list[str]] = None, social_media: Optional[bool] = False, proxy: str = None) -> None:
        super().__init__(query, filters, social_media, proxy)

    def start(self):
        if not self.social_media:
            captcha = self.isFoundCaptcha()
            jump = 0
            attr = None
            url = None
            if captcha:
                print("bing")
                jump = 11
                attr = self.url_attr["bing"]
                url = BINGSEARCH

            else:
                print("google")
                jump = 10
                attr = self.url_attr["google"]
                url = GOOGLESEARCH

            for i in range(0,self.page*10, jump):
                thread = Thread(target=self.searchQuery,args=(i,url,attr))
                thread.start()

            self.console.print(f"\t\t [bold green][[red]*[bold green]] THREAD : [purple]{active_count() - 1}{chr(32)*len(str(self.filter))}[/purple][bold green][[red]*[bold green]] QUERY : [purple]{self.query.replace('+',' ')}[/purple]")
            self.console.print(f"\t\t [bold green][[red]*[bold green]] FILTER : [/bold green]{self.filter} [bold green][[red]*[bold green]] SOCIAL-MEDIA : [purple]{self.social_media}[/purple]")
            self.console.progress_bar(active_count() - 1)
            self.event.set()
        else:
            self.social_data()
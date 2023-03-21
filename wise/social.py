from .const import userAgent,instagram_user_agents
from .proxy_checker import ProxyManager
from requests import Session
from bs4 import BeautifulSoup
from typing import Optional
from random import random

import re

VOID = None

class Twitter:
    def __init__(self) -> VOID:
        self.username = ""
        self.BEARER_CODE = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.user_agent = userAgent()
        self.result_data:list[tuple[str]] = []

    @property
    def __getGuestToken(self) -> int:
        with Session() as session:
            URL = "https://api.twitter.com/1.1/guest/activate.json"
            token = session.post(URL,headers={"authorization":self.BEARER_CODE})
            return token.json()["guest_token"]

    @property
    def __headers(self) -> dict[str,str]:
        return {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.BEARER_CODE,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-guest-token': self.__getGuestToken,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }

    def getUsers(self,slot) -> VOID:
        try:
            searched_on_twitter = self.__searchUser()
            screen_name = searched_on_twitter["users"][slot]["screen_name"]
            blue_tick = str(searched_on_twitter['users'][slot]["verified"])
            follower_count = self.__followerCount(screen_name)
            if blue_tick == "True":
                blue_tick = u'[blue]\u2713[/blue]'

            elif blue_tick == "False":
                blue_tick = "[bold][red]×[/red]"

            if follower_count == '0':
                follower_count = '[bold red]*[/bold red]'
            
            self.result_data.append((screen_name,follower_count,blue_tick))
        except IndexError:
            pass

    def __searchUser(self) -> dict[str,object]:
        with Session() as session:
            URL = "https://api.twitter.com/1.1/search/typeahead.json"
            params = {
                "include_ext_is_blue_verified":"1",
                "include_ext_verified_type":"1",
                "q":''.join(user+chr(32) for user in self.username).strip(),
                "src":"search_box",
                "result_type":"events%2Cusers%2Ctopics"
            }
            response = session.get(URL,headers=self.__headers,params=params).json()
            return response

    def __followerCount(self,username):
        with Session() as session:
            get_followers_count = session.get(f"https://api.twitter.com/1.1/users/show.json?screen_name={username}", headers=self.__headers)
            return str(get_followers_count.json()["followers_count"])

class Instagram:
    def __init__(self,proxy):
        self.proxy_manager = ProxyManager(proxy)
        self.result_data = {}
        self.data = []
        self.username = ""
        self.Uerror = False

    def getCSRFtoken(self) -> Optional[str]:
        with Session() as session:
            header = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"
            }
            URL = "https://www.instagram.com/accounts/login/"
            response = session.get(URL,headers=header)
            soup = BeautifulSoup(response.content,"lxml")
            regex = r".*csrf_token\":\"([^\"]+)\".*"
            scraping_script_tags = soup.find_all("script")
            for i in range(len(scraping_script_tags)):
                for j in scraping_script_tags[i]:
                    try:
                        token = j.split("XIGSharedData")[1][5:].replace('\\','')
                        match = re.match(regex, token)
                        if match:
                            return match.group(1)
                    except IndexError:
                        continue

    def userSearch(self) -> VOID:
        with Session() as session:
            headers = {
                "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "x-csrftoken" : self.getCSRFtoken(),
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            }
            params = {
                    "context": "blended",
                    "query": ''.join(user+chr(32) for user in self.username).strip(),
                    "rank_token": str(random()),
                    "count":1
                }
            URL = "https://www.instagram.com/web/search/topsearch/"
            response = session.get(URL,params=params,headers=headers,timeout=5)
            if response.status_code == 200:
                self.result_data = response.json()

    def getUsers(self,slot) -> VOID:
        try:
            username = self.result_data["users"][slot]["user"]["username"]
            followers = self.getFollowerCount(username)
            verified = str(self.result_data["users"][slot]["user"]["is_verified"])
            if verified == "True":
                verified = u'[blue]\u2713[/blue]'

            elif verified == "False":
                verified = "[bold][red]×[/red]"

            if followers == '0':
                followers = '[bold red]*[/bold red]'

            self.data.append((username,followers,verified))
        except IndexError:
            pass
        except KeyError:
            self.Uerror = True
    
    def getFollowerCount(self,username) -> str:
        with Session() as session:
            headers = {
                "user-agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_6) AppleWebKit/5352 (KHTML, like Gecko) Chrome/37.0.834.0 Mobile Safari/5352",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "content-type": 'text/html; charset="utf-8"',
            }
            response = session.get(f"https://www.instagram.com/{username}",headers=headers)
            soup = BeautifulSoup(response.content,"lxml")
            meta = []
            for i in soup.select("meta"):
                meta.append(i)

            followers = meta[16]
            followers = str(followers).split(' - ')
            return followers[0].removeprefix("<meta content=").split("Followers,")[0][1:].replace(',','')
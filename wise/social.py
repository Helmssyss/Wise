from requests import Session
from bs4 import BeautifulSoup
from .const import userAgent


class Twitter:
    def __init__(self,user:list=None) -> None:
        self.username = user
        self.BEARER_CODE = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.user_agent = userAgent()
        self.data = []

    @property
    def __getGuestToken(self) -> int:
        with Session() as session:
            URL = "https://api.twitter.com/1.1/guest/activate.json"
            token = session.post(URL,headers={"authorization":self.BEARER_CODE})
            return token.json()["guest_token"]

    @property
    def __headers(self):
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

    def get(self,slot):
        try:
            searched_on_twitter = self.__getUser()
            screen_name = searched_on_twitter["users"][slot]["screen_name"]
            location = searched_on_twitter["users"][slot]["location"]
            if location == '':
                location = '*'
            follower_count = self.__followerCount(screen_name)+" Follower"
            if follower_count == '0':
                follower_count = '*'
            self.data.append((screen_name,location,follower_count))
        except IndexError:
            pass

    def __getUser(self) -> dict:
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

class TikTok:
    @property
    def __header(self):
        return {
            "user-agent": userAgent(),
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json; charset=utf-8",
        }

    def isNotFoundUser(self,username):
        with Session() as session:
            r = session.get(f"https://www.tiktok.com/@{username}",headers=self.__header)
            _soup = BeautifulSoup(r.content,"lxml")
            notfound = _soup.find("p",attrs={"class":"tiktok-1c74ckh-PTitle emuynwa1"})
            if notfound:
                return True
            else:
                return False

    def getUser(self,username):
        if not self.isNotFoundUser(username):
            with Session() as session:
                r = session.get(f"https://www.tiktok.com/@{username}",headers=self.__header)
                _soup = BeautifulSoup(r.content,"lxml")
                data = {
                    "follow" : _soup.find("strong",attrs={"data-e2e":"following-count"}).text,
                    "followers" : _soup.find("strong",attrs={"data-e2e":"followers-count"}).text,
                    "likes" : _soup.find("strong",attrs={"data-e2e":"likes-count"}).text,
                    "bio" : _soup.find("h2",attrs={"data-e2e":"user-bio"}).text,
                    "videos": len(_soup.find_all("img",attrs={"class":"tiktok-1itcwxg-ImgPoster e1yey0rl1"})),
                }
                return data
        else:
            return "USER NOT FOUND!"
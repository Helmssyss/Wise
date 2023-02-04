from requests import Session
from bs4 import BeautifulSoup
from ..const import userAgent


class TikTok:
    @property
    def __header(self):
        return {
            "user-agent": userAgent(),
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json; charset=utf-8",
        }

    def getUser(self,username:list):
        with Session() as session:
            r = session.get(f"https://www.tiktok.com/@{''.join(user+chr(32) for user in username).strip()}",headers=self.__header)
            _soup = BeautifulSoup(r.content,"lxml")
            data = {
                "follow" : _soup.find("strong",attrs={"data-e2e":"following-count"}).text,
                "followers" : _soup.find("strong",attrs={"data-e2e":"followers-count"}).text,
                "likes" : _soup.find("strong",attrs={"data-e2e":"likes-count"}).text,
                "bio" : _soup.find("h2",attrs={"data-e2e":"user-bio"}).text,
                "videos": len(_soup.find_all("img",attrs={"class":"tiktok-1itcwxg-ImgPoster e1yey0rl1"})),
            }
            return data
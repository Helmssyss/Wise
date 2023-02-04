from requests import Session

class Twitter:
    def __init__(self,user_agent,user:list=None) -> None:
        self.username = user
        self.BEARER_CODE = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.user_agent = user_agent

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

    def get(self,slot,q):
        try:
            searched_on_twitter = self.__getUser()
            screen_name = searched_on_twitter["users"][slot]["screen_name"]
            location = searched_on_twitter["users"][slot]["location"]
            follower_count = self.__followerCount(screen_name)
            q.put((screen_name,location,follower_count))
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
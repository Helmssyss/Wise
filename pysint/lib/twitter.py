class Twitter:
    def __init__(self,request) -> None:
        self.request = request
        self.BEARER_CODE = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    
    @property
    def __getGuestToken(self) -> int:
        URL = "https://api.twitter.com/1.1/guest/activate.json"
        token = self.request.post(URL,headers={"authorization":self.BEARER_CODE})
        return token.json()["guest_token"]
    
    def getUser(self,username:list,useragent) -> dict:
        URL = "https://api.twitter.com/1.1/search/typeahead.json"
        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.BEARER_CODE,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': useragent,
            'x-guest-token': self.__getGuestToken,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }
        params = {
            "include_ext_is_blue_verified":"1",
            "include_ext_verified_type":"1",
            "q":''.join(user+chr(32) for user in username).strip(),
            "src":"search_box",
            "result_type":"events%2Cusers%2Ctopics"
        }
        response = self.request.get(URL,headers=headers,params=params).json()
        return response
    
    def followerCount(self,username:str):
        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.BEARER_CODE,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            'x-guest-token': self.__getGuestToken,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }
        get_followers_count = self.request.get(f"https://api.twitter.com/1.1/users/show.json?screen_name={username}", headers=headers)
        return get_followers_count.json()["followers_count"]
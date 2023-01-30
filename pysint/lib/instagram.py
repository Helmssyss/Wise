from requests import Session

def getProfile(username:str,user_agent) -> dict:
    with Session() as session:
        URL = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        header = {
            'Host':'i.instagram.com','Accept':'*/*',  'User-Agent': user_agent,
            'Cookie':'missing','Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US','X-IG-Capabilities':'3brTvw==',
            'X-IG-Connection-Type':'WIFI','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        }
        cookies = session.get("https://www.instagram.com",headers=header).cookies.get_dict()
        response = session.get(URL,headers=header,cookies=cookies)
        return response.json()
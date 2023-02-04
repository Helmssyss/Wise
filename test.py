# import requests

# AUTHORIZATION_KEY = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
# h = {
#     'authorization': AUTHORIZATION_KEY,
# }
# gt = requests.post('https://api.twitter.com/1.1/guest/activate.json', headers=h).json()['guest_token']

# headers = {
#             'authority': 'twitter.com',
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9',
#             'authorization': AUTHORIZATION_KEY,
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-origin',
#             'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
#             'x-guest-token': gt,
#             'x-twitter-active-user': 'yes',
#             'x-twitter-client-language': 'en',
# }
# response = requests.get('https://api.twitter.com/1.1/users/show.json?screen_name=jahreindota', headers=headers)
# print(response.json())

# # for i in range(10):
# #     print(response.json()["users"][i]["screen_name"])
# # a = [('jahreindota', 'Jahrein 😎', ''), ('jahrein_chat', "Jahrein'in Chati⚙️", 'Kampala, Uganda'), ('AkjennerJ', 'Jeral Akjener 🏵 #JahreininYanındayım', 'Jankara'), ('MevzuJahreine', 'Mevzu Jahrein’e', ''), ('Jahreincullen96', 'Rein-AU📌🍓🌿','Philippines🇵🇭'), ('Jahrein2023', 'Jahrein Kampanya', ''), ('dinom_r', 'Dinöm Hekim Hakları Komitesi⚙️#Jahreininyanındayım', ''), ('batuhxal', 'Batuh', 'Quenbec'), ('JahreinMikasa', 'caner', ''), ('CarlouiseJ', 'Carlouise Jahrein Jaspe', '')]

# # for screen_name,username,location in a:
# #     print(screen_name,username,location)

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json; charset=utf-8",
}
r = requests.get("https://www.tiktok.com/@x",headers=headers)
soup = BeautifulSoup(r.content,"lxml")
print(soup.find("p",attrs={"class":"tiktok-1c74ckh-PTitle emuynwa1"}))
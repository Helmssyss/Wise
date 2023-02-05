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

# from urllib.parse import urlparse

# print(urlparse("https://books.google.com.tr/books?id=EP5ureoiNosC&pg=PA63&lpg=PA63&dq=jahrein&source=bl&ots=39MDkXqYYJ&sig=ACfU3U0CQCzU_0Uuuoo2b-IsqzZEE8HLUA&hl=tr&sa=X&ved=2ahUKEwiF-8ji5v78AhVbpJUCHbYRAbQ4UBDoAXoECAMQAw").netloc)
# import re
# s = 'https://www.bing.com/ck/a?!&&p=e509d8d80660ad6dJmltdHM9MTY3NTU1NTIwMCZpZ3VpZD0xNWEzZGU1OS03MzM5LTZmYzgtMmU2MC1jY2Y2NzIzMzZlNTUmaW5aWQ9NTM5OA&ptn=3&hsh=3&fclid=15a3de59-7339-6fc8-2e60-ccf672336e55&psq=imamo%c4%9flu&u=a1aHR0cHM6Ly93d3cuc29uZGFraWthLmNvbS9wb2xpdGlrYS9zaWQ9NTM3NQ&ptn=3&hsh=3&fclid=15a3de59-7339-6fc8-2e60-ccf672336e55&psq=imamo%c4%9flu&u=a1aHR0cHM6Ly93d3cuZ2F6ZXRlZHV2YXIuY29tLnRyL2ltYW1vZ2x1bmRhbi1pc3RhbmJ1bGx1bGFyYS1rYXItdXlhcmlzaS1tdW1rdW4tb2xkdWd1LWthZGFyaXlsYS1kaXNhcml5YS1jaWtpbG1hbWFsaS1oYWJlci0xNjAxNzM3&ntb=1'
  
# # finding the protocol 
# obj1 = re.findall('://www.([\w\-\.]+)',s)
# print(obj1)



from bs4 import BeautifulSoup
import requests

user_name = "cznburak"
cookie = {}
verifyFp = cookie.get("s_v_web_id", "verify_kjf974fd_y7bupmR0_3uRm_43kF_Awde_8K95qt0GcpBk")
tt_webid = cookie.get("tt_webid", "6913027209393473025")
headers = {
            'Host': 't.tiktok.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Referer': 'https://www.tiktok.com/',
            'Cookie': 'tt_webid_v2=6913027209393473025; tt_webid=6913027209393473025'
}
url = "https://t.tiktok.com/@" + user_name
params = {
    "uniqueId": user_name,
    "validUniqueId": user_name,
}
r = requests.get(url,params=params,headers=headers)

print(r.text)

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
#     "accept": "*/*",
#     "accept-language": "en-US,en;q=0.9",
#     "content-type": "application/json; charset=utf-8",
# }
# r = requests.get("https://www.tiktok.com/@x",headers=headers)
# soup = BeautifulSoup(r.content,"lxml")
# print(soup.find("p",attrs={"class":"tiktok-1c74ckh-PTitle emuynwa1"}))
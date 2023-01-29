# import requests
# from random import choice

# def useragents():
#     dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
#     model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
#     pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
#     i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
#     user_agent = f'Instagram {choice(i_version)} Android (30/3.0; {choice(dpi_phone)}dpi; {choice(pxl_phone)}; huawei/google; {choice(model_phone)}; angler; angler; en_US)'
#     return user_agent
# data = {
#   "username":"zuck"
# }
# header = {
#   'Host':'i.instagram.com','Accept':'*/*',  'User-Agent': useragents(),
#   'Cookie':'missing','Accept-Encoding':'gzip, deflate',
#   'Accept-Language':'en-US','X-IG-Capabilities':'3brTvw==',
#   'X-IG-Connection-Type':'WIFI','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
# }
# # cookies = requests.get("https://www.instagram.com",headers=header).cookies.get_dict()
# print(requests.get("https://www.instagram.com/api/v1/users/web_profile_info/?username=zuck",headers=header).json())
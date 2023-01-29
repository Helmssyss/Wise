from random import choice

def instagram_user_agents():
    dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
    model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
    pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
    i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
    user_agent = f'Instagram {choice(i_version)} Android (30/3.0; {choice(dpi_phone)}dpi; {choice(pxl_phone)}; huawei/google; {choice(model_phone)}; angler; angler; en_US)'
    return user_agent

def userAgent() -> str :
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    ]
    return choice(agents)

GOOGLESEARCH = "https://www.google.com/search"
GOOGLEMAIN = "https://www.google.com/"
BINGSEARCH = "https://www.bing.com/search"
BINGMAIN = "https://www.bing.com/"
HEADER:dict[str,str] = {
    "user-agent": userAgent(),
    "accept-language": "en-US,en;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "content-type": "text/html; charset=utf-8"
}

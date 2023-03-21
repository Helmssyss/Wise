from requests import Session
from threading import Thread,Lock
from queue import Queue
from bs4 import BeautifulSoup
import os

VOID = None

class ProxyManager:
    worked_proxies:list[str] = []
    __threads:list[Thread] = []
    __safe:Lock = Lock()
    __que:Queue = Queue()
    isAlive = True
    def __init__(self,manager:str):
        self.manager = manager
        read_file = self.readFile()
        for i in read_file:
            self.__que.put(i)
        self.__manage()

    def readFile(self):
        if self.manager != None:
            if os.path.exists(self.manager):
                with open(self.manager,"r") as file:
                    for f in file: 
                        yield f.replace('\n','')

    def thrd(self,q:Queue):
        with Session() as session:
            while not q.empty():
                try:
                    prx = q.get()
                    proxies = {
                        "https": f"http://{prx}",
                        "http":f"http://{prx}"
                    }
                    response = session.get("https://httpbin.org/ip",proxies=proxies,timeout=5)
                    print(response.status_code,prx)
                    print(response.json())
                    if response.status_code == 200:
                        self.__safe.acquire()
                        self.worked_proxies.append(proxies)
                        self.__safe.release()
                        q.task_done()
                except Exception:
                    print("çalışmayan proxy, ",prx)
                    continue

    def __manage(self):
        for _ in range(30):
            t = Thread(target=self.thrd,args=(self.__que,)) 
            t.start() 
            self.__threads.append(t) 

        for thread in self.__threads: 
            thread.join()
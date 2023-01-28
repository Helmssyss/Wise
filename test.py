# # from distutils.spawn import find_executable
# # print(find_executable("make"))

# # import re

# # print(re.search(r"\b{0}\b".format("tiktok"),"https://www.tiktok.com/@cznburak/video/6768095078679465221").string)
# # a = "https://www.turkhackteam.org/konular/siberatay-temp-mail-botu-remake.2028134/qpo2ejqwporqw"

# # print(a[:77])

# from urllib.parse import urlparse

# print(urlparse("https://books.google.com.tr/books?id=6xB1EAAAQBAJ&pg=PA165&lpg=PA165&dq=elraenn&source=bl&ots=x3qMNXUvfG&sig=ACfU3U3ynUPFSGXFfXino5NQFXhcUAZY7A&hl=tr&sa=X&ved=2ahUKEwjjlIa6_-n8AhVhrJUCHXnyB4w4KBDoAXoECAIQA").netloc)

import threading
import time

def helper_function(event_obj, timeout,i):
  # Thread has started, but it will wait 10 seconds for the event  
  print("Thread started, for the event to set")
 
  flag = event_obj.wait(timeout)
  if flag:
    print("Event was set to true() earlier, moving ahead with the thread")
  else:
    print("Time out occured, event internal flag still false. Executing thread without waiting for event")
    print("Value to be printed=", i)
    
if __name__ == '__main__':
  # Initialising an event object
  event_obj = threading.Event()
  
  # starting the thread who will wait for the event
  thread1 = threading.Thread(target=helper_function, args=(event_obj,10,27))
  thread1.start()
  # sleeping the current thread for 5 seconds
  time.sleep(5)
  
  # generating the event
  event_obj.set()
  print("Event is set to true. Now threads can be released.")
  print()
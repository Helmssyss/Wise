import typing
import os


def proxies(path) -> typing.Generator:
    if os.path.exists(path):
        with open(file=path,mode='r') as file:
            for f in file:
                yield f.removesuffix("\n")
    else:
        return False
    
def asd():
    print(list(proxies(path=".\proxy_file.txt")))

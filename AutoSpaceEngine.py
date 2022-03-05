# Written By ef1500
# Auto Twitter space downloader Engine
# This is where it all comes together

import asyncio
import AutoTwitspaceDLX
import AutoSpaceEngineHandler as Yuzu
import concurrent.futures
import threading
import time
import os

BASE_PATH = "D:/Spaces/" # Base Directory (MUST END WITH SLASH)

def MakeDirs(Users):
    for User in Users:
        isFile = os.path.isdir(BASE_PATH+User)
        if isFile == False:
            os.mkdir(BASE_PATH+User)

def BeginMonitor(user):
    ustr = 'https://twitter.com/'+user
    AutoTwitspaceDLX.Monitor(ustr, BASE_PATH+user)

def Begin(user):
    ustr = 'https://twitter.com/'+user
    upath = BASE_PATH+user
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(AutoTwitspaceDLX.Monitor(ustr, upath))
    loop.close()
        

if __name__=="__main__":
    # I got the monitoring up and running. It works now!
    Users = AutoTwitspaceDLX.LoadData(BASE_PATH+'config.txt')
    MakeDirs(Users)
    ThreadLog = list()
    for user in Users:
        TwitThread = threading.Thread(target=Begin, args=(user,))
        ThreadLog.append(TwitThread)
        TwitThread.start()
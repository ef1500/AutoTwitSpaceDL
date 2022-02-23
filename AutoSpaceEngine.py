# Written By ef1500
# Auto Twitter space downloader Engine
# This is where it all comes together

import AutoTwitspaceDLX
import AutoSpaceEngineHandler as Yuzu
import threading
import time
import os

BASE_PATH = "D:/Spaces/" # Base Directory (MUST END WITH SLASH)

def MakeDirs(Users):
    for User in Users:
        isFile = os.path.isdir(BASE_PATH+str(User))
        if isFile == False:
            os.mkdir(BASE_PATH+str(User))

def BeginMonitor(user):
    ustr = 'https://twitter.com/'+str(user)
    AutoTwitspaceDLX.Monitor(ustr, BASE_PATH+str(user))

if __name__=="__main__":
    # I got the monitoring up and running. It works now!
    Users = AutoTwitspaceDLX.LoadData(BASE_PATH+'config.txt')
    MakeDirs(Users)
    ThreadLog = list()
    for user in Users:
        TwitThread = threading.Thread(target=BeginMonitor, args=(user,))
        ThreadLog.append(TwitThread)
        TwitThread.start()
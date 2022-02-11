# Written By ef1500
# Auto Twitter space downloader Engine
# This is where it all comes together

import AutoTwitspaceDLX
import os

BASE_PATH = "D:/Spaces/" # Base Directory (MUST END WITH SLASH)
NOTIF_URL = "WEBHOOK_URL" # Discord Webhook url for the notification

def MakeDirs(Users):
    for User in Users:
        isFile = os.path.isdir(BASE_PATH+str(User))
        if isFile == False:
            os.mkdir(BASE_PATH+str(User))

def BeginMonitor(Users):
    for user in Users:
        ustr = 'https://twitter.com/'+str(user)
        AutoTwitspaceDLX.Monitor(ustr, BASE_PATH+str(user))

if __name__=="__main__":
    # I don't actually have a clue how to make a monitor that would run in the background, restarting
    # Whenever a twitter space ends, so until I figure that out, this will have to do.
    Users = AutoTwitspaceDLX.LoadData(BASE_PATH+'config.txt')
    MakeDirs(Users)
    BeginMonitor(Users)

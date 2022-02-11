# Written by ef1500
# Automatic Twitter Space Downloader

import os
import re
import json
import glob
import requests
import subprocess
import DiscordNotifEngine


#Let's define some important variables
BASE_PATH = "D:/Spaces/" # Base Directory (MUST END WITH SLASH)
NOTIF_URL = "WEBHOOK_URL" # Discord Webhook url for the notification

# First we want to be able to read a file that contains all of the
# Users that we would like to monitor for a twitter space. We can do this with the help of a text file
# This will also save us time when we are preparing for the discord integration to send an embed.

def LoadData(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    return data

# Great. Now we've got our little "Mini" Data Loader Ready, now lets begin monitoring for a twitter space.

# If a twitter space is starting, send a discord message via webhook signaling that the specified user is now live.
# When that user is no longer live, begin uploading the file to a temporary storage site
# Once completed, Return the link via webhook (This should be replaced by the autoTorrent program to autoUpload to Holopirates)

def CheckLive(user, path):
    # Here we want to create a function that checks if the specified user is live
    # If they are live, send a discord notification, if not, then check again
    checkLive = subprocess.Popen("twspace_dl -U "+user+" --write-url urls.txt -s", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path)
    ox, ex = checkLive.communicate()
    checkLive.wait() #Wait for the process to end
    # Now check to see if there is a urls.txt file in the folder that contains the url
    isFile = os.path.isfile(path+'/'+'urls.txt')
    if isFile == True:
        DiscordNotifEngine.GenerateEmbed(NOTIF_URL, "", "Ongoing Space", "Now archiving... Will be uploaded momentarily", "Twitter Space Notification System", "https://imgur.com/E2vh4aa.png", user)
        os.remove(path+'/'+'urls.txt') #Now delete the file
        return True

def Monitor(user, path):
    isLive = CheckLive(user,path)
    # Open A Subprocess to begin the downloading process
    if isLive == True:
        monitor = subprocess.Popen("twspace_dl -o [%(creator_name)s%(id)s]-%(title)s -U "+user, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path) #Open the process in the specific directory so that way we don't have any interference when uploading to tempupload.
        # Small note - We have to make the twsapce filename weird because if there's hangul, sometimes windows will throw an error and then the downloader will fail to pull through. I've got no idea how to fix this
        # Put the output and error in their own variables (Communicate returns two values.)
        ox, ex = monitor.communicate()

        AutoUpload(path, user) # Begin The Autoupload process

# Now to create the function that automatically uploads the most recent file in the folder to the tempupload service
# Let's start by making the function that finds the most recent file in a folder
def FindLatest(path, user):
    lf = glob.glob(path+'/'+'*') # Path must end in /
    nwf = max(lf, key=os.path.getctime)
    return str(nwf) # Return The latest file

#Autoupload function
def AutoUpload(path, user):
    # Find the latest file in the folder
    file = FindLatest(path, user)

    #Str(file) can cause an error to get thrown if the filename isn't supported by windows, and transfersh upload won't occur.
    upload = subprocess.Popen("transfersh "+str(file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path)
    oy, ey = upload.communicate()
    upload.wait()
    print(oy, ey)
    if not ey:
        # Regex The link out
        urlReg = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        u = urlReg.search(str(oy))
        ux = str(u.group())
        # Notify Via Discord
        DiscordNotifEngine.GenerateEmbed(NOTIF_URL, ux[:-6], "Space us Uploaded!", "Finished Archiving!", "Mizusawa Alert System", "https://imgur.com/nGQWo3C.png", user)

# Written by ef1500
# Automatic Twitter Space Downloader

import os
import re
import json
import time
import glob
import requests
import subprocess
import DiscordNotifEngine
import AutoSpaceEngineHandler as Yuzu # Yes I'm using waifu names for imports

#Let's define some important variables
BASE_PATH = "D:/Spaces/" # Base Directory (MUST END WITH SLASH)
NOTIF_URL = "Your Webhook Url" # Discord Webhook url for the notification
INTERVAL = 45 # The interval for the monitor to sleep (In Seconds)

# First we want to be able to read a file that contains all of the
# Users that we would like to monitor for a twitter space. We can do this with the help of a text file
# This will also save us time when we are preparing for the discord integration to send an embed.
# Make sure that your config file is in the same place where all of your spaces are going to be downloaded.

def LoadData(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    f.close()
    return data

# Great. Now we've got our little "Mini" Data Loader Ready, now lets begin monitoring for a twitter space.

# If a twitter space is starting, send a discord message via webhook signaling that the specified user is now live.
# When that user is no longer live, begin uploading the file to a temporary storage site
# Once completed, Return the link via webhook (This should be replaced by the autoTorrent program to autoUpload to Holopirates)



def CheckLive(user, user_id, token):
    ustr = user[20:]
    # Here we want to create a function that checks if the specified user is live
    # If they are live, send a discord notification, if not, then check again
    # Update: Since I rethought the mechanism for this, the underlying process is located in the AutoSpaceHandler
    # Update 2: Twitter didn't like me generating guest tokens every 3 seconds so I started getting a rate limit of sorts, so I'll move the
    # function below and change the args on this function.
    isSpace = Yuzu.CheckIfSpace(user_id, token)
    isLive = Yuzu.CheckIfLive(isSpace, token)

    if isLive == True:
        spaceInfo = Yuzu.getSpaceInfo(isSpace, token) # Get the information about the twitter space

        #Strings for the embed
        spaceUrl = "**Space Url:** " + '\n' + 'https://twitter.com/i/spaces/' + spaceInfo[1] + '\n' + '\n'
        spaceTitleStr = "**Space Title:** " + '\n' + str(spaceInfo[0]) + '\n' + '\n'
        spaceIDstr = "**Space ID:**" + '\n' + str(spaceInfo[1]) + '\n'

        #Join all of the strings
        des = ''.join(spaceTitleStr + spaceUrl + spaceIDstr)

        # Now generate the notification
        DiscordNotifEngine.GenerateEmbed(NOTIF_URL, " ", ustr + " Is hosting a twitter space!", des, ustr, 'https://imgur.com/E2vh4aa.png', ustr)
        return True
    else:
        return False

def Monitor(user, path):
    token = Yuzu.getGuest() # Let's change this so it's now only a one-time process and it's not called all the time.
    UserID = lambda user : Yuzu.GetUserID(user) # Slap the old function in a lambda, it's nicer that way!
    isLive = CheckLive(user, UserID(user), token) # Initial Check to define the variable

     # Now we begin writing the actual monitor of the program
    while isLive != True:
        isLive = CheckLive(user, UserID(user), token) # Check if the user is live (as always)
        time.sleep(INTERVAL) # Now Just sleep for the specified interval before doing it again. (Should I use async here because I'm working with threads?)

    if isLive == True:
        # Open A Subprocess to begin the downloading process
        monitor = subprocess.Popen("twspace_dl -o [%(creator_screen_name)s_%(id)s]-%(start_date)s -U "+user, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path) #Open the process in the specific directory so that way we don't have any interference when uploading to tempupload.
        # Small note - We have to make the twsapce filename weird because if there's hangul, sometimes windows will throw an error and then the downloader will fail to pull through. I've got no idea how to fix this
        # Put the output and error in their own variables (Communicate returns two values.)
        ox, ex = monitor.communicate()
        try:
            AutoUpload(path, user) # Begin The Autoupload process
        except:
            pass


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
    if not ey:
        # Regex The link out
        urlReg = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        u = urlReg.search(str(oy))
        ux = str(u.group())
        # Notify Via Discord
        DiscordNotifEngine.GenerateEmbed(NOTIF_URL, ux[:-6], "Space is Uploaded!", "Finished Archiving!", "Mizusawa Alert System", "https://imgur.com/nGQWo3C.png", user[20:])

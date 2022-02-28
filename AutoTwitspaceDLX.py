# Written by ef1500
# Automatic Twitter Space Downloader

# Normal Imports
import os
import re
import json
import time
import glob
import requests
import subprocess
import DiscordNotifEngine
import AutoSpaceEngine
import AuthEngine as kronii
import AutoSpaceEngineHandler as Yuzu # Yes I'm using waifu names for imports
import multiprocessing
from twspace_dl import Twspace
from twspace_dl import TwspaceDL


#Let's define some important variables
BASE_PATH = "D:/Spaces/" # Base Directory (MUST END WITH SLASH)
NOTIF_URL = "Your Webhook URL" # Discord Webhook url for the notification
INTERVAL = 5 # The interval for the monitor to sleep (In Seconds)

# First we want to be able to read a file that contains all of the
# Users that we would like to monitor for a twitter space. We can do this with the help of a text file
# This will also save us time when we are preparing for the discord integration to send an embed.
# Make sure that your config file is in the same place where all of your spaces are going to be downloaded.

def LoadData(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f if not (line.startswith('$') or line.startswith('\n'))] # Use $ As a comment, so it's a bit more detailed (if you want)
    f.close()
    return data

# Great. Now we've got our little "Mini" Data Loader Ready, now lets begin monitoring for a twitter space.

# If a twitter space is starting, send a discord message via webhook signaling that the specified user is now live.
# When that user is no longer live, begin uploading the file to a temporary storage site
# Once completed, Return the link via webhook (This should be replaced by the autoTorrent program to autoUpload to Holopirates)

def CheckLive_(user):
    isSpace = Yuzu.CheckIfSpace_(user, kronii.GetToken(kronii.LoadTokens(BASE_PATH+'tokens.txt')))
    if isSpace == False:
        return False
    if isinstance(isSpace, str) == True:
        isLive = Yuzu.CheckIfLive_(isSpace)
        if isLive == True:
            xSpace = Twspace._metadata(isSpace)

            spaceUrl = "**Space Url:** " + '\n' + 'https://twitter.com/i/spaces/'+xSpace['data']['audioSpace']['metadata']["rest_id"] + '\n' + '\n'

            try:
                spaceTitleStr = "**Space Title:** " + '\n' + xSpace['data']['audioSpace']['metadata']["title"] + '\n' + '\n'
            except:
                spaceTitleStr = "**Space Title:** " + '\n' + user[20:] +'\'s'+" Space" + '\n' + '\n'
            spaceIDstr = "**Space ID:**" + '\n' + xSpace['data']['audioSpace']['metadata']["rest_id"] + '\n'
            des = ''.join(spaceTitleStr + spaceUrl + spaceIDstr)

            DiscordNotifEngine.GenerateEmbed(NOTIF_URL, " ", user[20:] + " Is hosting a twitter space!", des, user[20:], 'https://imgur.com/E2vh4aa.png', user[20:])

            return True
        else:
            return False

def Monitor(user, path):
#    token = Yuzu.getGuest() # Let's change this so it's now only a one-time process and it's not called all the time.
#    UserID = lambda user : Yuzu.GetUserID(user) # Slap the old function in a lambda, it's nicer that way!
    space_id = Yuzu.CheckIfSpace_(user, kronii.GetToken(kronii.LoadTokens(BASE_PATH+'tokens.txt')))
    TwitSpace = TwspaceDL(space_id, format_str="(%(creator_name)s)%(title)s-%(id)s")
    isLive = CheckLive_(user) # Initial Check to define the variable
     # Now we begin writing the actual monitor of the program
    while isLive != True:
        isLive = CheckLive_(user) # Check if the user is live (as always)
        time.sleep(INTERVAL) # Now Just sleep for the specified interval before doing it again. (Should I use async here because I'm working with threads?)

    if isLive == True:
        # Open A Subprocess to begin the downloading process
        monitor = subprocess.Popen("twspace_dl -o [%(creator_screen_name)s_%(id)s]-%(start_date)s -U "+user, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path) #Open the process in the specific directory so that way we don't have any interference when uploading to tempupload.
        #Monitor = multiprocessing.Process(target=TwitSpace.download, args=(path,))
        #Monitor.start()
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
    print("Upload started!")
    # Find the latest file in the folder
    file = FindLatest(path, user)

    #Str(file) can cause an error to get thrown if the filename isn't supported by windows, and transfersh upload won't occur.
    upload = subprocess.Popen("transfersh "+str(file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path)
    oy, ey = upload.communicate()
    print(oy, ey)
    upload.wait()
    if not ey:
        # Regex The link out
        urlReg = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        u = urlReg.search(str(oy))
        ux = str(u.group())

        # Create Strings for the embed
        uploadUrl = ux[:-6]
        up_user = user[20:]

        # Define some extra strings and then  construct the embed
        upStr = "**Upload URL:**" + '\n' + uploadUrl + '\n' + '\n'
        noteStr = "*Note: All links will expire after 300 hours*" + '\n'
        des = ''.join(upStr + noteStr)

        # Notify Via Discord
        DiscordNotifEngine.GenerateEmbed(NOTIF_URL, " ", up_user + "'s Twitter Space is Ready for download", des, up_user, "https://imgur.com/nGQWo3C.png", user[20:])

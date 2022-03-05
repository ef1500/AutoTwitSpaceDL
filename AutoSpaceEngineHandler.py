# Twitter Space Automatic Downloader/Monitor Rewrite
# Written by ef1500
# The old one wasn't working and I was getting frustrated with it, so I've decided to wrtite the Whole Damn thing myself, with the help of others. 
import json
import AutoTwitspaceDLX as Yuu
from twspace_dl import Twspace
from twspace_dl import twitter
import TwUser
import AuthEngine

def CheckIfSpace_(username, auth_token):
    # Get the User's ID and store it
    user = TwUser.tUser(username[20:])
    # Aight Now that we've got that out of the way, let's check if the user is live
    if auth_token:
        try:
            s_id = Twspace.from_user_avatar(user.TwURL, auth_token) # Space ID
            return s_id['id']
        except:
            return False
    else:
        try:
            s_id = Twspace.from_user_tweets(user.TwURL)
            print(s_id)
            return s_id
        except:
            return False

def CheckIfLive_(space_id):
    tSpace = Twspace._metadata(space_id)
    if tSpace["data"]["audioSpace"]["metadata"]["state"] == "Running":
        return True
    if tSpace["data"]["audioSpace"]["metadata"]["state"] == "Ended":
        return False
    else:
        return False
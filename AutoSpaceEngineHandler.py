# Twitter Space Automatic Downloader/Monitor Rewrite
# Written by ef1500
# The old one wasn't working and I was getting frustrated with it, so I've decided to wrtite the Whole Damn thing myself, with the help of others. 
import re
import json
import requests
import twspace_dl

# Grab a guest token for usage on the twitter api
def getGuest():
    guestActivate = 'https://api.twitter.com/1.1/guest/activate.json'

    res = requests.post(guestActivate, headers={
                        'Authorization': 'Bearer ' + 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'})

    return res.json()['guest_token']

# Get the user ID so we can pass it on and check if the user is live
def GetUserID(user):
    UserID = twspace_dl.TwspaceDL.user_id(user)
    return UserID

def CheckIfLive(user_id):
    headers = {
        "authorization": (
        "Bearer "
        "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
        "=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        ),
        "x-guest-token": getGuest(),
    }
    params = {
        "variables": (
            "{"
            f'"userId":"{user_id}",'
            '"count":20,'
            '"withTweetQuoteCount":true,'
            '"includePromotedContent":true,'
            '"withQuickPromoteEligibilityTweetFields":false,'
            '"withSuperFollowsUserFields":true,'
            '"withUserResults":true,'
            '"withNftAvatar":false,'
            '"withBirdwatchPivots":false,'
            '"withReactionsMetadata":false,'
            '"withReactionsPerspective":false,'
            '"withSuperFollowsTweetFields":true,'
            '"withVoice":true}'
        )
    }
    response = requests.get(
        "https://twitter.com/i/api/graphql/jpCmlX6UgnPEZJknGKbmZA/UserTweets",
        params=params,
        headers=headers,
    )
    tweets = response.text
    try:
        space_id = re.findall(r"(?<=https://twitter.com/i/spaces/)\w*", tweets)[0]
    except (IndexError, json.JSONDecodeError) as err:
        return False
    return True

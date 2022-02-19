# Twitter Space Automatic Downloader/Monitor Rewrite
# Written by ef1500
# The old one wasn't working and I was getting frustrated with it, so I've decided to wrtite the Whole Damn thing myself, with the help of others. 
import re
import json
import requests
import functools as mei
import twspace_dl as Shizuku

# Grab a guest token for usage on the twitter api
def getGuest():
    guestActivate = 'https://api.twitter.com/1.1/guest/activate.json'
    res = requests.post(guestActivate, headers={'Authorization': 'Bearer ' + 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'})
    return res.json()['guest_token']

# Get the user ID so we can pass it on and check if the user is live
@mei.lru_cache(maxsize=128)
def GetUserID(user):
    UserID = Shizuku.twspace_dl.TwspaceDL.user_id(user)
    print("I'm Getting the id for " + user)
    return UserID

# Small Note - I just realized that this will find any and all spaces on that account, so if one is ongoing, then you're straight outta luck 
# If you want to monitor new spaces.
# However, we can make use of this! It's not entirely pointless. We can use this to check if there's a space, and then we can return the link 
# of the onging space so we can hand it over to a function that will check if the twitter space is still ongoing or not. 
def CheckIfSpace(user_id, token):
    headers = {
        "authorization": (
        "Bearer "
        "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
        "=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        ),
        "x-guest-token": token, # I think that this is where our error stems from. I think that if we stop generating tokens all the time and make this a one-time process, it will work flawlessly.
    }
    params = {
        "variables": (
            "{"
            f'"userId":"{user_id}",'
            '"count": 5,' # We can look at the most recent tweet every second, as if we're monitoring every second, we're allowed 900 requests per 15 minutes. This should eliminate the guest token error. Update: That didn't solve anything.
            '"withTweetQuoteCount":false,' # Stop quote tweets from plauging our query
            '"includePromotedContent":false,' # Who wants that garbage?
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
        return space_id
    except (IndexError, json.JSONDecodeError) as err:
        return False # Is this a bad idea? We'll see I guess lol 
    # Update: Changed from None to False. Could be the stem of my issue.

# Now we need to make a checker that will rapidly check to see if the space is live or not so that way we can 
# Start the recording process.
def CheckIfLive(space_id, token):
    params = {
        "variables": (
            "{"
            f'"id":"{space_id}",'
            '"isMetatagsQuery":false,'
            '"withSuperFollowsUserFields":true,'
            '"withUserResults":true,'
            '"withBirdwatchPivots":false,'
            '"withReactionsMetadata":false,'
            '"withReactionsPerspective":false,'
            '"withSuperFollowsTweetFields":true,'
            '"withReplays":true,'
            '"withScheduledSpaces":true'
            "}"
            )
    }

    headers = {
        "authorization": (
            "Bearer "
            "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
            "=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
            ),
            "x-guest-token": token, #edit here too
    }
    response = requests.get("https://twitter.com/i/api/graphql/jyQ0_DEMZHeoluCgHJ-U5Q/AudioSpaceById",params=params, headers=headers)

    meta = response.json()

    try:
        if meta["data"]["audioSpace"]["metadata"]["state"] == "Ended":
            return False
        if meta["data"]["audioSpace"]["metadata"]["state"] == "TimedOut":
            return False
        else:
            return True
    except KeyError:
        return False

def getSpaceInfo(space_id, token):
    params = {
        "variables": (
            "{"
            f'"id":"{space_id}",'
            '"isMetatagsQuery":false,'
            '"withSuperFollowsUserFields":true,'
            '"withUserResults":true,'
            '"withBirdwatchPivots":false,'
            '"withReactionsMetadata":false,'
            '"withReactionsPerspective":false,'
            '"withSuperFollowsTweetFields":true,'
            '"withReplays":true,'
            '"withScheduledSpaces":true'
            "}"
            )
    }

    headers = {
        "authorization": (
            "Bearer "
            "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
            "=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
            ),
            "x-guest-token": token, #edit here too
    }
    response = requests.get("https://twitter.com/i/api/graphql/jyQ0_DEMZHeoluCgHJ-U5Q/AudioSpaceById",params=params, headers=headers)

    meta = response.json()

    try:
        title = meta["data"]["audioSpace"]["metadata"]["title"] # Get the title for the embed
    except KeyError:
        title = "None Provided"
    rest_id = meta["data"]["audioSpace"]["metadata"]["rest_id"] # Get the Space ID while we're at it too

    return title, rest_id
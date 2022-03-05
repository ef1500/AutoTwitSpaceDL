# AuthEngine
# Written by ef1500
# Written so that we can bypass the use of proxies, and still monitor an absurd amount of users.
import functools as kaede
import requests
import time
from functools import lru_cache
import random

# Create a functions that allows us to load up all of the user tokens and store them in a list that's cached so we can
# call it efficently later on
@kaede.lru_cache(maxsize=256)
def LoadTokens(file):
    with open(file, 'r') as TokenLoader:
        tokens = [line.strip() for line in TokenLoader]
    TokenLoader.close()
    return tokens
    
# Let's now make another function that will let us spread the amount of monitored users across multiple accounts
def GetToken(tokens):
    if len(tokens) <= 1:
        return tokens[0]
    else:
        return tokens[random.randrange(len(tokens))] # Return a random token

@lru_cache(maxsize=256)
def getGuest(ttl_hash=None):
    del ttl_hash # we're not using this, we're simply gonna use it to exploit the cache to update every hour.
    guestActivate = 'https://api.twitter.com/1.1/guest/activate.json'
    res = requests.post(guestActivate, headers={'Authorization': 'Bearer ' + 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'})
    return res.json()['guest_token']

def get_ttl_hash(seconds=3600):
    return round(time.time()/seconds)

# Now to make this update on the hour, just call token = getGuest(ttl_hash=get_ttl_hash())

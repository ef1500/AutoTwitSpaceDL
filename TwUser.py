
# Twitter User Class
# Create a class for the twitter user
# Written by ef1500
import requests
import time
from functools import cached_property, lru_cache
from cachetools import func

class tUser:
    def __init__(self, username):
        self.User = username
        self.TwURL = f"https://twitter.com/{username}"

    @staticmethod
    def GetUserID(u_url):
        # Let's put the code to get the user's ID here.
        # Thanks to ryu for helping me on this one.
        params = {"screen_names" : u_url[20:]} # Set the params
        response = requests.get("https://cdn.syndication.twimg.com/widgets/followbutton/info.json", params=params,) # Send out a request
        uDat = response.json() # Pack the response into json
        return uDat[0]["id"]
# Discord Notification Engine
# Written by ef1500
# This is meant to serve as a simple way to construct a simplistic embed from a single function so that way 
# We can conserve space and neatly customize the embeds.
import json
import requests

#Generate an embed 
def GenerateEmbed(Url, content, Title, Desc, Name, IconUrl, user):
    data = {"content":content, "username": user} 
    # Content is an actual message, not in the embed, and the username is the username of the webhook

    data["embeds"] = [
        {
            "title": Title, # Embed Title
            "description": Desc, # Description of the embed (Put the text you want in the embed here)
            "author": {
                "name": Name, # The Author Name 
                "icon_url": IconUrl # The Url of the author icon
        },
            "color": 15406156, # Color of the embed
            "footer": {
                "text": "Powered by ef1500", # Footer Text
                "icon_url": "https://imgur.com/nGQWo3C.png" # Footer Icon
                }
            }
        ]

    sendNotif = requests.post(Url, json=data)
    try:
        sendNotif.raise_for_status()
    except requests.exceptions.HTTPError as exx:
        print(exx)
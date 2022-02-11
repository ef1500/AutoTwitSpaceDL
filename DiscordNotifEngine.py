# Discord Notification Engine
# Written by ef1500
# This is meant to serve as a simple way to construct a simplistic embed from a single function so that way 
# We can conserve space and neatly customize the embeds.
import json
import requests

def GenerateEmbed(Url, content, Title, Desc, Name, IconUrl, user):
    data = {"content":content, "username": user[20:]}
    # We Have to add the [20:] There because in the main file we added https://twitter.com/ to the front of the username, so we're just removing that. 

    data["embeds"] = [
        {
            "title": Title,
            "description": Desc,
            "author": {
                "name": Name,
                "icon_url": IconUrl
        },
            "color": 15406156,
            "footer": {
                "text": "Powered by ef1500",
                "icon_url": "https://imgur.com/nGQWo3C.png"
                }
            }
        ]

    sendNotif = requests.post(Url, json=data)
    try:
        sendNotif.raise_for_status()
    except requests.exceptions.HTTPError as exx:
        print(exx)
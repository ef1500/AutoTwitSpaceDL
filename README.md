# AutoTwitSpaceDL
Automatic Twitter Space Downloader and Uploader with Discord integration

# What it does
- Monitors A list of users for Twitter Spaces
- Notifies you via discord webhook
- Uploads a temporary archive of the twitter space to transfer.sh so you can share it with friends

An example of the program in action is shown below

![Example Space Archive](https://imgur.com/clrnIND.png)

It's not the best, but I'm working to make it the best I can.

# Setting up
## What you'll need
- A twitter account
- Discord webhook url
- Folder for all of the twitter spaces to be downloaded to

## Preparing a config
The config file is really simple, all you have to do is create a file titled config.txt in the folder you want all of the spaces to be downloaded and put the usernames of the users you would like to monitor. I've provided a small example.

You can add a '$' to add comments if you'd like.

![Example Config.txt File](https://imgur.com/xBudh8A.png)

## Adding your path to the code
- Copy the path of your spaces folder
- Next, navigate to the location you cloned the repo
- Open the files "AutoSpaceEngine.py" and "AutoTwitspaceDLX.py" and edit the BASE_PATH string to your desired path. (Please note it must end with a slash!)

Do not worry about the folders shown in the example, they will be created for you automatically ;)

![Example Path](https://imgur.com/Y2VQncS.png)

![Example Path2](https://imgur.com/65FzoBI.png)

## Adding your discord webhook to the code
- Copy the URL for your webhook
- Next, navigate to the location you cloned the repo
- Open the file "AutoTwitspaceDLX.py" and edit the NOTIF_URL to your discord webhook URL.

## Adding twitter auth tokens
In order for the program to work properly and reliably, you must specify an auth token. This will allow you to get space IDs even if the user did not tweet about it, and it will also allow you to monitor exponentially more accounts at once.
I reccomend that you make a new account specifically for archiving spaces. 
### Getting your auth token
If you have chrome, use the extension 'EditThisCookie'. It will allow you to easily copy the cookie.
Copy the value for the cookie titled 'auth_token'. Do not share it.

![EditThisCookieEX](https://imgur.com/AVc1r0N.png)

Once you have this value copied, head over to the same place your config is located and created a new file called 'tokens.txt'.

## Running the program
Once you're ready to go, just open up the python console type

```python
pip install -r requirements.txt
```
This will get all the required dependencies up and running. Once you've got everything installed, simply type

```python
python3 AutoSpaceEngine.py
```
The program will now begin the monitoring and upload process. 

IMPORTANT NOTE: Ctrl+C will not stop this program. You either click the x button or exit via task manager.

## Customizing the embed
In the file "DiscordNotifEngine.py", the arguments for the embed are explained so that you can edit the embed.


# TODO
- Also allow for the option to automatically create torrents and upload them to mogu.holopirates.moe in addition (or not) to the tempupload feature
- Allow for the Customization of the Author/Footer images and footer text
- More detailed embeds (With the url embedded!) -- Done!
- Multiple Webhook support (maybe)
- Restarting a thread after a space is finished archivng
- Make a nice looking cli (Maybe) -- In the works!

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
- Discord webhook url
- Folder for all of the twitter spaces to be downloaded to

## Preparing a config
The config file is really simple, all you have to do is create a file titled config.txt in the folder you want all of the spaces to be downloaded and put the usernames of the users you would like to monitor. I've provided a small example.

![Example Config.txt File](https://imgur.com/AaSllYJ.png)

## Adding your path to the code
- Copy the path of your spaces folder
- Next, navigate to the location you cloned the repo
- Open the files "AutoSpaceEngine.py" and "AutoSpaceEngineHandler.py" and edit the BASE_PATH string to your desired path. (Please note it must end with a slash!)

Do not worry about the folders shown in the example, they will be created for you automatically ;)

![Example Path](https://imgur.com/Y2VQncS.png)

![Example Path2](https://imgur.com/65FzoBI.png)

## Adding your discord webhook to the code
- Copy the URL for your webhook
- Next, navigate to the location you cloned the repo
- Open the files "AutoSpaceEngine.py" and "AutoSpaceEngineHandler.py" and edit the NOTIF_URL to your discord webhook URL.

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
The function is called in AutoTwitspaceDLX.py on lines 48 and 100.


# TODO
- Also allow for the option to automatically create torrents and upload them to mogu.holopirates.moe in addition (or not) to the tempupload feature
- Allow for the Customization of the Author/Footer images and footer text
- More detailed embeds (With the url embedded!)
- Multiple Webhook support (maybe)
- Make a nice looking cli (Maybe)

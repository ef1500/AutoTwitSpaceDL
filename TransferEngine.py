# Transfer.sh Upload engine
# Modified from transfersh-cli python package
import os
import requests

URL_TRANSFERSH = 'https://transfer.sh'

def transfersh_upload(filename, max_days, max_downloads):
    """ Program that uploads a file to Transfer.sh """
    try:
        # Open file
        with open(filename, 'rb') as data:
            conf_file = {filename: data}
            headers = {}
            # Option to indicate the maximum number of days
            if max_days is not None:
                headers['Max-Days'] = str(max_days)
            # Option to indicate the maximum number of downloads
            if max_downloads is not None:
                headers['Max-Downloads'] = str(max_downloads)
            r = requests.post(URL_TRANSFERSH, files=conf_file, headers=headers)
            # Shows route to download
            download_url = r.text
            # Copy route to clipboard
            return download_url
    except Exception:
        print('Something has failed. The file could not be uploaded.')
# YTsync
A python script for converting a YouTube playlist to mp3 files and pushing them to another folder for device synchronisation

## Requirements
* python 2.7+
* pip install youtube_dl

## Usage
python path_to_file/sync.py -p playlist_url [-l path_to_sync_folder]

### Explanation
The script does the following:
* downloads all of the videos in the playlist and converts them to mp3 files
* saves the mp3 files in an output directory (in the same place as the script)
* if path_to_sync_folder is specified, it will also copy all of the mp3 files to the sync folder

### My Setup
* Windows Task Scheduler to automatically run the script at 10pm every night
* sync folder is a folder in my Dropbox account
* on my phone I have ["Dropsync"](https://play.google.com/store/apps/details?id=com.ttxapps.dropsync) installed which will automatically download and delete files from my sync folder when I'm connected to WiFi

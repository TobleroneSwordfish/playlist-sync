# Playlist sync
An all in one python script that handles syncing a youtube playlist to your phone.

Made because I have a deep seated need for offline access to my trash sadgirl music at all times and refuse to pay google for the privilege.

Handles:
- Downloading the playlist
- Copying the playlist onto your phone
- Keeping track of files you already have downloaded and skipping them
- Deleting files from the disk and phone when removed from the playlist

Does not currently handle:
- Multiple playlists
- Automatic dependency setup

## Supports
Anything that can run python -> Android.

# Does not support
iPhones.

iPhone users can pay $29.99 a month for iTunes ultra cloud golden special limited edition as is the natural order of the universe.

## Requirements
### yt-dlp
https://github.com/yt-dlp/yt-dlp

Needed to download videos.

NB: You may need to keep this updated as youtube continue fighting their shadow war against downloader utilities.

### Python
https://www.python.org/downloads/

Needed for yt-dlp.

### adb
https://developer.android.com/tools/releases/platform-tools

Needed to copy files onto your android phone.

## Setup
- Download all of the requirements and either add them to your path or put them directly in this folder.
- Put your playlist and preferred options into `config.txt`.
- Enable USB debugging on your phone: http://web.archive.org/web/20220706143529/https://developer.android.com/training/basics/firstapp/running-app.html#RealDevice
- Plug in your phone.
- Run `sync.bat`
- Tadaa

## Disclaimer
This uses an adb shell and is running "rm" commands. It should be doing so in a safe way but just be aware of that. I am not responsible if you manage to find a way to brick your phone with this script.
# README.md

## SQ-Labs Lesson Downloader.

### Installation:
- Clone Repo `git clone <URL>  `
- Build image using Dockerfile `sudo docker build -t "sq-downloader" .` (This will take some time.)
- Run the image and launch the container make sure to replace /path/to/downloads_folder to a relevant path on your system.
`sudo docker run -it -v /path/to/downloads_folder/:/root/Downloads/ --rm --name sq-downloader`
this will run the container interactivly presenting a prompt menu.
- Follow the menu to download a specific clip or to download all of them.

## Under the hood.
This code will download a txt file from Google Drive, parse the lines into a list if dictionaries, 
each containing a Lesson Number, Lesson Date, Link and Passcode.

Once the parsing is finished, the user will be presented with a menu that allows
downloading all clips or, downloading a single (specific) clip.
Choosing to download a specific clip, the user will be presented with the table of available clips,
mentioning the lesson numbers and dates. Choosing the clip by lesson number and pressing ENTER will start the download.

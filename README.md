# README.md
## SQ-Labs Lesson Downloader.
### Installation:
- Clone Repo `git clone <URL>  `
- Build image using Dockerfile `sudo docker build -t "sq-downloader" .` (This will take some time.)
- Run the image and launch the container make sure to replace /path/to/downloads_folder to a relevant path on your system.
`sudo docker run -it -v /path/to/downloads_folder/:/root/Downloads/ --rm --name sq-downloader`
this will run the container interactivly presenting a prompt menu.
- Follow the menu to download a specific clip or to download all of them.

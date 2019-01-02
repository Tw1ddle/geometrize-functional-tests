import os
import platform
import subprocess

systemName = platform.system()

if systemName != "Windows" and systemName != "Mac" and systemName != "Linux":
    raise Exception("Unknown operating system, don't know what application version to download")

if systemName != "Linux":
	raise Exception("This only works on Linux for now, Windows/Mac would work but need additional setup for app installation, extra browser prompts etc")
	
# Browser to use, note we do redirects etc based on client side js so can't just use wget
browser = 'google-chrome-stable'
	
# Folder structure on download page is windows/mac/linux
breadcrumb = systemName.lower()

# Path to the latest installer/app binary
breadcrumb_url = 'https://s3.amazonaws.com/geometrize-installer-bucket/index.html?breadcrumb=' + breadcrumb + '%2F'
latest_download_url = breadcrumb_url + '&dl_latest=true'

# Run browser, expect download to happen
subprocess.call([browser, latest_download_url], shell=False)
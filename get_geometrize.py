import glob
import os
from os.path import expanduser
import platform
import shutil
import subprocess
import time

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

print("Creating browser downloads directory")

homeDir = os.path.expanduser('~')

os.makedirs(homeDir + "/Downloads")

print("Will download the application through the web browser")

subprocess.call([browser, latest_download_url], shell=False)

print("Waiting for 2 minutes for the web browser download the application...")

time.sleep(120)

print(os.listdir(homeDir))

# Path to the Chrome downloads directory (assuming this is the right place)
downloadsDir = homeDir + '/Downloads'

# Look for the downloaded Geometrize binary
downloadedFiles = os.listdir(downloadsDir)

print("Will print downloaded files...")

print(downloadedFiles)

filteredDownloads = glob.glob(downloadsDir + '/geometrize*')

print(filteredDownloads)

if not filteredDownloads:
    raise Exception("Failed to find the downloaded application binary")

filePath = os.abspath(filteredDownloads[0])

print("Will copy the app to the testing subfolder")

shutil.copy(os.abspath(filePath), os.path.realpath(__file__) + "/app/Geometrize.AppImage")
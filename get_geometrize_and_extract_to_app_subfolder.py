# This script downloads the latest Geometrize installer/binaries for each platform
# It then installs/unpacks the downloads to the /app subfolder
# Note that to do this on Windows, it runs the Windows installer for Geometrize in unattended mode

import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import urllib
import urllib.parse
import urllib.request

socket.setdefaulttimeout(600) # Downloading shouldn't take this long, idea is to cause a timeout

# Helper for preventing divide by zero in download progress callback
def safe_divide(x, y):
    if y == 0:
        return 0
    return x / y

# Progress callback when downloading the Geometrize installer/executables
def downloadProgressCb(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(safe_divide(progress_size, (1024 * duration)))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" % (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

script_dir = os.path.dirname(os.path.realpath(__file__))

system_name = platform.system()

if system_name != "Windows" and system_name != "Darwin" and system_name != "Linux":
    raise Exception("Unknown operating system, don't know what app version to download")

# Folder structure has windows/osx/linux at its base
breadcrumb = None
if system_name == "Windows":
    breadcrumb = "windows"
elif system_name == "Darwin":
    breadcrumb = "osx"
elif system_name == "Linux":
    breadcrumb = "linux"

# Default to MSVC builds for Windows
if breadcrumb == "windows":
    breadcrumb = "windows/msvc2019_64"

bucket_url = 'https://geometrize-installer-bucket.s3.amazonaws.com/'

# URL for file containing the name of the latest binary, which we ought to download and test with
latest_tag_url = bucket_url + breadcrumb + "/__latest"

print("Searching for file containing name of build to test with at: " + latest_tag_url)

latest_url_file_name = '__latest'
urllib.request.urlretrieve(latest_tag_url, latest_url_file_name)
binary_file_name = open(latest_url_file_name ,"r").read().strip()

print("Latest file is named " + binary_file_name + " - will download to repo root")

latest_binary_url = bucket_url + urllib.parse.quote_plus(breadcrumb + "/" + binary_file_name)
urllib.request.urlretrieve(latest_binary_url, binary_file_name, downloadProgressCb)

print("Finished downloading!")

source_path = script_dir + "/" + binary_file_name
target_path = script_dir + "/app"

# Remove and then recreate the /app destination folder, initially
if os.path.exists(target_path):
    shutil.rmtree(target_path)

# Create the app folder
if not os.path.exists(target_path):
    os.makedirs(target_path)

# Unpack/install binary to "app" folder, same place for all platforms for symmetry
if system_name == "Windows":
    print("Installing app to app folder in unattended mode")
    unattended_installer_path = script_dir + "/windows_unattended_install_script.qs"
    subprocess.check_call([source_path, '--script', unattended_installer_path])
else:
    print("Copying app from " + source_path + " to " + target_path)

    if system_name == "Darwin":
        shutil.copyfile(source_path, target_path + "/Geometrize.dmg")
    elif system_name == "Linux":
        shutil.copyfile(source_path, target_path + "/Geometrize.AppImage")

print(os.listdir(target_path))
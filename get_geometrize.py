import os
import platform
import shutil
import subprocess
import urllib
import urllib.request

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

script_dir = os.path.dirname(os.path.realpath(__file__))

system_name = platform.system()

if system_name != "Windows" and system_name != "Mac" and system_name != "Linux":
    raise Exception("Unknown operating system, don't know what app version to download")

# Folder structure has windows/mac/linux at its base
breadcrumb = system_name.lower()

# Default to MSVC builds for Windows
if breadcrumb == "windows":
    breadcrumb = "windows/msvc2015_64"

bucket_url = 'https://geometrize-installer-bucket.s3.amazonaws.com/'

# URL for file containing the name of the latest binary, which we ought to download and test with
latest_tag_url = bucket_url + breadcrumb + "/__latest"

print("Searching for file containing name of build to test with at: " + latest_tag_url)

latest_url_file_name = '__latest'
urllib.request.urlretrieve(latest_tag_url, latest_url_file_name)
binary_file_name = open(latest_url_file_name ,"r").read().strip()

print("Latest file is named " + binary_file_name + " - will download to app subfolder")

latest_binary_url = bucket_url + urllib.parse.quote_plus(breadcrumb + "/" + binary_file_name)
urllib.request.urlretrieve(latest_binary_url, "app/" + binary_file_name)

print("Finished downloading!")

source_path = script_dir + "/app/" + binary_file_name
target_path = script_dir + "/app/app_prepared"

# Unpack/install binary to "app_prepared" folder, same place for all platforms for symmetry
if system_name == "Windows":
    print("Installing app to /app_prepared folder in unattended mode")
    unattended_installer_path = script_dir + "/windows_unattended_install_script.qs"
    subprocess.check_call([source_path, '--script', unattended_installer_path])
else:
    print("Copying app from " + source_path + " to " + target_path)

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if system_name == "Mac":
        shutil.copyfile(source_path, target_path + "/Geometrize.dmg")
    elif system_name == "Linux":
        shutil.copyfile(source_path, target_path + "/Geometrize.AppImage")

print(os.listdir(target_path))
import os
import platform
import shutil
import subprocess
import urllib
import urllib.parse

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
urllib.urlretrieve(latest_tag_url, latest_url_file_name)
binary_file_name = open(latest_url_file_name ,"r").read().strip()

print("Latest file is named " + binary_file_name + " - will download to repo root")

latest_binary_url = bucket_url + urllib.parse.quote_plus(breadcrumb + "/" + binary_file_name)
urllib.urlretrieve(latest_binary_url, binary_file_name)

print("Finished downloading!")

source_path = script_dir + "/" + binary_file_name
target_path = script_dir + "/app"

# Unpack/install binary to "app" folder, same place for all platforms for symmetry
if system_name == "Windows":
    print("Installing app to app folder in unattended mode")
    unattended_installer_path = script_dir + "/windows_unattended_install_script.qs"
    subprocess.check_call([source_path, '--script', unattended_installer_path])
else:
    print("Copying app from " + source_path + " to " + target_path)

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if system_name == "Darwin":
        shutil.copyfile(source_path, target_path + "/Geometrize.dmg")
    elif system_name == "Linux":
        shutil.copyfile(source_path, target_path + "/Geometrize.AppImage")

print(os.listdir(target_path))
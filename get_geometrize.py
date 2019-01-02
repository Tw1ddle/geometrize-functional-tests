import platform
import urllib
import urllib.parse
import urllib.request

systemName = platform.system()

if systemName != "Windows" and systemName != "Mac" and systemName != "Linux":
    raise Exception("Unknown operating system, don't know what app version to download")

# Folder structure has windows/mac/linux at its base
breadcrumb = systemName.lower()

# Default to MSVC builds for Windows
if breadcrumb == "windows":
    breadcrumb = "windows/msvc2015_64"

bucket_url = 'https://geometrize-installer-bucket.s3.amazonaws.com/'

# URL for file containing the name of the latest binary, which we ought to download and test with
latest_tag_url = bucket_url + breadcrumb + "/__latest"

print("Searching for file containing name of build to test with at: " + latest_tag_url)

latest_url_file_name = '__latest'
urllib.request.urlretrieve(latest_tag_url, latest_url_file_name)
latest_file_name = open(latest_url_file_name ,"r").read().strip()

print("Latest file is named " + latest_file_name + " - will download to app subfolder")

latest_binary_url = bucket_url + urllib.parse.quote_plus(breadcrumb + "/" + latest_file_name)
urllib.request.urlretrieve(latest_binary_url, "app/" + latest_file_name)

print("Finished downloading!")
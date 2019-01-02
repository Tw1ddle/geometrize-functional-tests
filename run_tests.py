import glob
import platform
import os
import stat
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))

system_name = platform.system()
binary_name = None

if system_name == "Windows":
    binary_name = "Geometrize.exe"
elif system_name == "Darwin":
    binary_name = "Geometrize.dmg"
elif system_name == "Linux":
    binary_name = "Geometrize.AppImage"
else:
    raise Exception("Unknown operating system, don't know how to run the tests")

binary_path = script_dir + "/app/" + binary_name
tests_dir = script_dir + "/tests"
results_dir = script_dir + "/results"

tests_option = "--functional_tests=" + tests_dir

if system_name == "Windows":
    print("Running Windows executable")
    subprocess.check_call([binary_path, tests_option])
elif system_name == "Darwin":
    mount_point = "/Volumes/Geometrize/"
    print("Mounting Mac .dmg to " + mount_point)
    subprocess.check_call(["hdiutil", "attach", "-mountpoint", mount_point, binary_path])

    print("Finding Mac .app")
    
    # https://bugreports.qt.io/browse/QTBUG-60324 - dmg structure is the
    # current working directory when the build was done... so we must find the .app file
    matches = []
    for filepath in glob.iglob(mount_point + '**/Geometrize.app', recursive=True):
        matches.append(filepath)

    print(matches)
    if not matches:
        raise Exception("Failed to find Geometrize.app file")
    
    app_path = matches[0]
    
    print("Running Mac .app")
    subprocess.check_call(["/usr/bin/open", "-W", "-n", "-a", app_path, "--args", tests_option])

elif system_name == "Linux":
    print("Making AppImage executable")
    st = os.stat(binary_path)
    os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
    
    print("Running Linux AppImage")
    subprocess.check_call([binary_path, tests_option])
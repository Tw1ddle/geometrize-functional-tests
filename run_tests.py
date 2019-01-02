import platform
import os
import stat
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))

system_name = platform.system()
binary_name = None

if system_name == "Windows":
    binary_name = "Geometrize.exe"
elif system_name == "Mac":
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
elif system_name == "Mac":
    print("Mounting Mac .dmg")
    subprocess.check_call(["sudo hdiutil", "attach", binary_path])
    
    print("Running Mac executable")
    subprocess.check_call(["/Volumes/Geometrize/Geometrize.app", tests_option])
elif system_name == "Linux":
    print("Making AppImage executable")
    st = os.stat(binary_path)
    os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
    
    print("Running the Linux app image")
    subprocess.check_call([binary_path, tests_option])
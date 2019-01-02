import platform
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = script_dir + "/app/app_prepared"

system_name = platform.system()

if system_name == "Windows":
    
elif system_name == "Mac":
    
elif system_name == "Linux":

else:
    raise Exception("Unknown operating system, don't know how to run the tests")
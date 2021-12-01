import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
results_dir = script_dir + "/results"
results_files = os.listdir(results_dir)

if len(results_files) <= 1: # There may be 1 file which is just a .gitkeep file
    print('Found no test results in the results folder ' + results_dir + ' ... counting this as a test failure')
    sys.exit(1)

test_fail_string = "FAIL"
found_failures = 0

for file_name in results_files:
    if os.path.isfile(results_dir + os.sep + file_name):
        f = open(results_dir + os.sep + file_name, 'r')

        file_contents = f.read()
        if test_fail_string in file_contents:
            print('Found one or more FAILs in file %s' % file_name)
            print('File content was: ' + file_contents)
            found_failures += 1

        f.close()

if (found_failures > 0):
    print('\n\nFound ' + str(found_failures) + ' failures. Tests failed\n\n')
    sys.exit(1)

print('\n\nTests passed without reporting any failures to the results folder\n\n')
sys.exit(0)
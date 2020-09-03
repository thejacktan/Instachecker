import functions as my_fun
from glob import glob
from os.path import expanduser
from sqlite3 import connect
from pathlib import Path
import instaloader

L = instaloader.Instaloader(max_connection_attempts=1)
my_target = str(input("Profile you want to analyze: "))
print("You have selected username: " + my_target)

saved_session_files = glob(str(instaloader.instaloader.get_default_session_filename(username='') + "*"))
session_list = []
if not saved_session_files:
    print("There are no locally saved session files!")
    my_username = str(input("Username you want to login with: "))
else:
    for my_file in saved_session_files:
        temp_name = Path(my_file).stem.split('-')[-1]
        session_list.append(temp_name)
    print("The following accounts have locally saved sessions: ")
    print(session_list)
    my_username = str(input("Username you want to login with (Press enter to use first in list): "))
    if not my_username:
        my_username = session_list[0]
    print("you have selected: " + my_username)

# Try login from saved session file
try:
    L.load_session_from_file(my_username)
except FileNotFoundError:
    print("Session file for " + my_username + " has not yet been created. Attempting to copy cookies from Firefox!"
                                              " Make sure you have logged in on Firefox!")
    # Note that this differs between operating systems, default has been set to windows location
    my_cookies = glob(expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release/cookies.sqlite"))[0]
    # noinspection PyProtectedMember
    L.context._session.cookies.update(connect(my_cookies)
                                      .execute("SELECT name, value FROM moz_cookies WHERE host='.instagram.com'"))
    try:
        username = L.test_login()
        if not username:
            raise instaloader.ConnectionException()
    except instaloader.ConnectionException:
        raise SystemExit("Cookie import failed. Are you logged in successfully in Firefox? Cookie path used is: " +
                         my_cookies)
    L.context.username = username
    L.save_session_to_file()
    print("Successfully saved cookie files for instagram profile " + L.context.username)

my_start = str(input("Start date (YYYY-MM-DD), leave blank for default: "))
my_end = str(input("End date (YYYY-MM-DD), leave blank for default: "))

# Input arguments into functions
my_fun.get_data(target_name=my_target, my_instance=L)
my_fun.analyze_data(target_name=my_target, from_date=my_start, to_date=my_end)

print('Done!')

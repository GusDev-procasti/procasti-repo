"""

Procasti!_OS Installer Preparer System v1.0

"""

#libs
from colorama import Fore as fore, Style as style, Back, init
from pathlib import Path as p
import subprocess as sub
import sys
from time import sleep as s

#colorama configs and variables
init(autoreset=True)
remover = style.RESET_ALL
info = fore.GREEN + "[INFO]" + remover + ": "
error = fore.RED + "[ERROR]" + remover + ": "

#path variables
installer_desktop = p("/home/installer/Desktop")

#system DEFs
def boot():
    print("Welcome to Procasti!_OS installer preparer!")
    s(0.3)
    sub.run(["useradd", "-m", "-u", "2011", "installer"])
    sub.run(["passwd", "-d", "installer"])
    print(info + "installer user created.")
    sub.run("passwd", input="1234\n1234\n", text=True)
    print(info + "root password defined as '1234'.")
    sub.run(["usermod", "-aG", "wheel,root", "installer"])
    print(info + "installer received all groups.")
    sub.run(["pacman", "-Syyu", "--noconfirm"])
    print(info + "all repositories connected.")
    if installer_desktop.exists() and installer_desktop.is_dir():
        print(info + "installer desktop folder found.")
        copy_desktop()
    else:
        print(error + "installer desktop folder not found. Creating...")
        sub.run(["mkdir", "/home/installer/Desktop"])
        print(info + "installer desktop folder found.")
        copy_desktop()

def copy_desktop():
    sub.run(["cp", "/usr/local/bin/.procastios/install-system.desktop", "/home/installer/Desktop"])
    print(info + "installer desktop copied to installer dekstop folder successfully.")
    begin()

def begin():
    print("everything is done. Want begin the installation?")
    while True:
        choose = input("option selected[Y/n]: ")
        if choose.strip() == "":
            print(info + "this part is empty. Using preset 'y'.")
            choose = 'y'
            break
        else:
            if choose in ['y', 'Y', 's', 'S'] or choose in ['n', 'N']:
                break
            else:
                print(error + "this option is not valid.")
                continue
    if choose in ['y', 'Y', 's', 'S']:
        sub.run(["systemctl", "enable", "lightdm", "--now"])
    elif choose in ['n', 'N']:
        print("Installer preprarer finished.")
        sys.exit()

if __name__ == "__main__":
    boot()
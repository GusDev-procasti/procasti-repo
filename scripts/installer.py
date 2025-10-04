"""

Procasti!_OS Installer system

"""

#libs
from colorama import Fore as fore, Style as style, Back, init
import subprocess as sub
import sys
import pyfiglet
from pathlib import Path as p
from time import sleep as s

#colorama config variables
init(autoreset=True)
remover = style.RESET_ALL
info = fore.GREEN + "[INFO]" + remover + ": "
error = fore.RED + "[ERROR]" + remover + ": "

#path variables
os_release = p("/mnt/etc/os-release")

#variables
title = pyfiglet.figlet_format("Procasti!_OS")
global_name = None

#system DEFs
def boot():
    print(f"\n{title}\n")
    print("Welcome to Procasti!_OS Installer!")
    print("Made by: GusDev.")
    print("Want begin the installation?")
    while True:
        resp = input("option selected[Y/n]: ")
        if resp.strip() == "":
            print(error + "this part is empty. Using preset 'y'.")
            resp = 'y'
            break
        else:
            if resp in ['y', 'Y', 's', 'S'] or resp in ['n', 'N']:
                break
            else:
                print(error + "this option is not valid.")
                continue
    if resp in ['y', 'Y', 's', 'S']:
        disk_selector()
    elif resp in ['n', 'N']:
        print("Installation aborted.")
        sys.exit()

def disk_selector():
    print(info + "booting disk-selector...")
    s(0.3)
    sub.run(["sudo", "fdisk", "-l"])
    print("select an disk to install the Procasti!_OS system.")
    while True:
        resp = input("disk selected: ")
        if resp.strip() == "":
            print(error + "this part cannot be empty.")
            continue
        else:
            if resp.startswith("/dev/"):
                if resp.strip() == "/dev/loop0":
                    print(error + "you cannot install Procasti!_OS system on your installer disk.")
                    continue
                else:
                    print(info + fore.RED + "EVERYONE " + remover + "file will be deleted. Are you sure?")
                    while True:
                        choose = input("option selected[y/N]: ")
                        if choose.strip() == "":
                            print(info + "this part is empty. Using preset 'n'.")
                            choose = 'n'
                            break

                        else:
                            if choose in ['y', 'Y', 's', 'S'] or choose in ['n', 'N']:
                                break
                            else:
                                print(error + "this option is not valid.")
                    if choose in ['y', 'Y', 's', 'S']:
                        partitioner(resp)
                        break
                    elif choose in ['n', 'N']:
                        print("disk-selector aborted. Rebooting...")
                        disk_selector()
                        break
            else:
                print(error + "this disk is not valid.")

def partitioner(disk: None):
    print(info + "boot partitioner...")
    s(0.3)
    print(info + f"trying make GPT label on {disk}...")
    sub.run(["sudo", "umount", "-R", "/mnt"])
    sub.run(["sudo", "parted", "-s", disk, "mklabel", "gpt"])
    print(info + "disk formated to GPT.")
    print(info + "Trying to make boot partition...")
    sub.run(["sudo", "parted", "-s", disk, "mkpart", '"EFI system partition"', "fat32", "1MiB", "1025MiB"])
    sub.run(["sudo", "parted", "-s", disk, "set", "1", "esp", "on"])
    print(info + "boot partition created successfully.")
    print("want linux-swap?")
    while True:
        resp = input("option selected[Y/n]: ")
        if resp.strip() == "":
            print(error + "this part is empty. Using preset 'y'.")
            resp = 'y'
            break
        else:
            if resp in ['y', 'Y', 's', 'S'] or resp in ['n', 'N']:
                break
            else:
                print(error + "this option is not valid.")
                continue
    if resp in ['y', 'Y', 's', 'S']:
        print(info + "trying to make swap partition...")
        sub.run(["sudo", "parted", "-s", disk, "mkpart", '"linux swap partition"', "linux-swap", "1025MiB", "5121MiB"])
        print(info + "swap partition created successfully.")
        print(info + "trying to make root partition...")
        sub.run(["sudo", "parted", "-s", disk, "mkpart", '"root partition"', "ext4", "5121MiB", "100%"])
        sub.run(["sudo", "parted", "-s", disk, "type", "3", "4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709"])
        print(info + "root partition created successfully.")
        print(info + "every thing is done.")
        formatter(disk=disk, swap=True)
    elif resp in ['n', 'N']:
        print(info + "swap will be not created.")
        print(info + "trying to make root partition...")
        sub.run(["sudo", "parted", "-s", disk, "mkpart", '"root partition"', "ext4", "1025MiB", "100%"])
        sub.run(["sudo", "parted", "-s", disk, "type", "2", "4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709"])
        print(info + "root partition created successfully.")
        formatter(disk=disk, swap=False)




def formatter(disk: None, swap: bool = True):
    print(info + "booting formatter...")
    s(0.3)
    print(info + "trying format boot partition...")
    sub.run(["sudo", "mkfs.fat", "-F", "32", f"{disk}1"])
    if swap == True:
        print(info + "boot partition formatted successfully.")
        print(info + "trying format swap partition...")
        sub.run(["sudo", "mkswap", f"{disk}2"])
        print(info + "swap partition created successfully.")
        print(info + "trying to format root partition...")
        sub.run(["sudo", "mkfs.ext4", f"{disk}3"])
        print(info + "root partition created successfully.")
        mounter(disk=disk, swap=True)
    elif swap == False:
        print(info + "boot partition formatted successfully.")
        print(info + "trying to format root partition...")
        sub.run(["sudo", "mkfs.ext4", f"{disk}2"])
        print(info + "root partition created successfully.")
        mounter(disk=disk, swap=False)



def mounter(disk: None, swap: bool = True):
    print(info + "booting mounter...")
    s(0.3)
    if swap == True:
        print(info + "trying mount all disk...")
        sub.run(["sudo", "mount", f"{disk}3", "/mnt"])
        print(info + "root partition mounted successfully.")
        sub.run(["sudo", "mount", "--mkdir", f"{disk}1", "/mnt/boot"])
        print(info + "boot partition mounted successfully.")
        sub.run(["sudo", "swapon", f"{disk}2"])
        print(info + "swap partition mounted successfully.")
        print(info + "all disk partitions are mounted.")
        install_root_minimal()
    elif swap == False:
        print(info + "trying mount all disk...")
        sub.run(["sudo", "mount", f"{disk}3", "/mnt"])
        print(info + "root partition mounted successfully.")
        sub.run(["sudo", "mount", "--mkdir", f"{disk}1", "/mnt/boot"])
        print(info + "boot partition mounted successfully.")
        print(info + "all disk partitions are mounted.")
        install_root_minimal()


def install_root_minimal():
    print(info + "booting install-system...")
    s(0.3)
    print(info + "trying to install minimal system...")
    sub.run(["sudo", "pacstrap", "-K", "/mnt", "base", "linux", "linux-firmware", "sudo", "nano", "networkmanager", "e2fsprogs", "man-pages", "man-db", "texinfo"])
    print(info + "system root installed successfully.")
    sub.run(["sudo", "genfstab", "-U", "/mnt", ">>", "/mnt/etc/fstab"])
    print(info + "fstab generated successfully.")
    print("choose an password for root user.")
    while True:
        choose = input("password: ")
        if choose.strip() == "":
            print(error + "this part cannot be empty.")
            continue
        else:
            break
    sub.run(["sudo", "arch-chroot", "/mnt", "passwd"], input=f"{choose}\n{choose}\n", text=True)
    print(info + "root user password defined.")
    print("type your username.")
    while True:
        username = input("username: ")
        if username.strip() == "":
            print(error + "this part cannot be empty.")
            continue
        else:
            global_name = username
            break
    print(f"type the password for user: '{username}'.")
    while True:
        user_pass = input(f"{username} password: ")
        if user_pass.strip() == "":
            print(error + "this part cannot be empty.")
            continue
        else:
            break
    sub.run(["sudo", "arch-chroot", "/mnt", "useradd", "-m", username])
    sub.run(["sudo", "arch-chroot", "/mnt", "passwd", username], input=f"{user_pass}\n{user_pass}\n", text=True)
    print(info + "user created successfully.")
    print(info + "minimal system installed successfully.")
    s(0.3)
    bootloader_installer(username=username)

def bootloader_installer(username: str = None):
    print(info + "booting booloader-installer...")
    s(0.3)
    sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "grub", "efibootmgr", "--noconfirm"])
    print(info + "bootloader installer installed successfully.")
    sub.run(["sudo cp /usr/local/bin/.procastios/assets/procasti/grub /mnt/etc/default/"])
    s(0.3)
    sub.run(["sudo", "arch-chroot", "/mnt", "grub-install", "--target=x86_64-efi", "--efi-directory=/boot", "--bootloader-id=GRUB"])
    sub.run(["sudo", "arch-chroot", "/mnt", "grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
    print(info + "bootloader installed successfully.")
    print(info + "the minimal system is installed. Want procced?")
    while True:
        resp = input("option selected[Y/n]: ")
        if resp.strip() == "":
            print(error + "this part is empty. Using preset 'y'.")
            resp = 'y'
            break
        else:
            if resp in ['y', 'Y', 's', 'S'] or resp in ['n', 'N']:
                break
            else:
                print(error + "this option is no valid.")
                continue
    if resp in ['y', 'Y', 'S', 's']:
        personalizer(username=username)
    elif resp in ['n', 'N']:
        print(info + "install finished.")
        sub.run(["sudo", "arch-chroot", "/mnt", "systemctl", "enable", "NetworkManager", "--now"])
        sub.run(["sudo", "umount", "-R", "/mnt"])
        s(0.5)
        print(info + "network system booted.")
        sys.exit()

def personalizer(username: str = None):
    print(info + "booting personalizer...")
    s(0.3)
    sub.run(["sudo", "cp", "/usr/local/bin/.procastios/assets/procasti/popi", "/mnt/usr/local/bin"])
    sub.run(["sudo", "cp", "/usr/local/bin/.procastios/assets/procasti/popi-updater", "/mnt/usr/local/bin"])
    sub.run(["sudo", "chmod", "+x", "/mnt/usr/local/bin/popi-updater"])
    sub.run(["sudo", "chmod", "+x", "/mnt/usr/local/bin/popi"])
    print(info + "POPI installed.")
    sub.run(["sudo", "mkdir", "/mnt/usr/share/procasti"])
    print(info + "Procasti!_OS assets folder created.")
    sub.run(["sudo", "cp", "/usr/local/bin/.procastios/assets/procasti/procasti.png", "/mnt/usr/share/procasti"])
    print(info + "logo installed.")
    sub.run(["sudo", "rm", "-rf", os_release])
    sub.run(["sudo", "cp", "/usr/local/bin/.procastios/assets/procasti/os-release", "/mnt/etc"])
    print(info + "os-release installed.")
    sub.run(["sudo", "cp", "/usr/local/bin/.procastios/assets/procasti/hostname", "/mnt/etc"])
    print(info + "hostname defined.")
    sub.run(["sudo", "rm", "/mnt/ent/issue"])
    sub.run(["sudo", "cp", "/usr/local/bin/.procastios/assets/procasti/issue", "/mnt/etc"])
    print(info + "issue installed.")
    print("want one DE(Desktop Environment)?")
    print("options:\n1 - Kde Plasma.\n2 - Gnome.\n3 - XFCE.")
    while True:
        resp = input("option selected[default=nothing.]: ")
        if resp.strip() == "":
            print(error + "this part is empty. Using preset 'nothing'.")
            resp = None
            break
        else:
            try:
                choose = int(resp)
                break
            except ValueError:
                print(error + "type an valid number.")
                continue
    if choose == 1:
        print(info + "Selected: KDE Plasma.")
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman -S", "plasma", "kde-applications", "--noconfirm"])
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "firefox", "--noconfirm"])
        print(info + "KDE Plasma installed.")
        sub.run(["sudo", "arch-chroot", "/mnt", "systemctl", "enable", "sddm", "--now"])
        print(info + "KDE Plasma installation finished.")
        finalizer()
    elif choose == 2:
        print(info + "Selected: GNOME.")
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "gnome", "gnome-extra.", "--noconfirm"])
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "firefox", "--noconfirm"])
        print(info + "GNOME installed.")
        sub.run(["sudo", "arch-chroot", "/mnt", "systemctl", "enable", "gdm", "--now"])
        print(info + "GNOME installation finished.")
        finalizer()
    elif choose == 3:
        print(info + "Selected: XFCE.")
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "xfce4", "xfce4-goodies", "--noconfirm"])
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "firefox", "--noconfirm"])
        print(info + "XFCE installed.")
        sub.run(["sudo", "arch-chroot", "/mnt", "pacman", "-S", "lightdm", "lightdm-gtk-greeter", "--noconfirm"])
        print(info + "lightdm installed.")
        sub.run(["sudo", "arch-chroot", "/mnt", "systemctl", "enable", "lightdm", "--now"])
        print(info + "XFCE installation finished.")
        finalizer()
    else:
        print(error + "no option found. Using no DE.")
        finalizer(username=username)

def finalizer(username: str = None):
    print(info + "booting finalizer...")
    s(0.3)
    sub.run(["sudo", "arch-chroot", "/mnt", "systemctl", "enable", "NetworkManager", "--now"])
    print(info + "network system enabled.")
    print(info + "Procasti!_OS installed. Want shutdown?[Y/n]: ")
    while True:
        choose = input("option selected: ")
        if choose.strip() == "":
            print(error + "this part is empty. Using preset 'y'.")
            choose = 'y'
        else:
            if choose in ['y', 'Y', 's', 'S'] or choose in ['n', 'N']:
                break
            else:
                print(error + "this option is not valid.")
                continue
    if choose in ['y', 'Y', 's', 'S']:
        print("Thanks to install Procasti!_OS :)")
        s(1.5)
        sub.run(["shutdown", "now"])
    elif choose in ['n', 'N']:
        print("Thanks to install Procasti!_OS :)")
        s(1.5)
        sys.exit()


        
    
if __name__ == "__main__":
    boot()
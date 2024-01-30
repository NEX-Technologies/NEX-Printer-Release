#!/usr/bin/python3

"""
This script is used for running the start up main 
program and checking if USB update is available, 
specifically:

- Opens a UI.

- Checks if there is a update zip file named 
G3D-Printer-Release-master.zip in the root of flash drive.
- Extracts it at user's download's directory.
- Read the config in the extracted version.
- Read the current config of the currend program.
- Display info about the current and new version.

- Allows the user to update/downgrade on button click
or cancel it.
- Start the program.

- If there is no update file in the root usb directory,
the program will simply start the program in user's
home directory indicated by the path:

/home/user/G3D-Printer/build/G3D-Printer 

DO NOT EDIT OR MODIFY THIS FILE
G3D Software Development Team
"""

import os
import getpass
import shutil
import zipfile
import time
import sys
import subprocess
import re

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi

def read_config(path, key):

    try:
        with open(path, "r", newline="") as f:

            for line in f:

                if line.startswith(key):
                    target = line.strip()
                    key, val = target.split("=")
                    key = key.strip()
                    val = val.strip()

                    print(key, val)
        return val

    except Exception as exp:
        print(str(exp))

    return ""

# Variable constants.
TARGET_FILE_NAME = "G3D-Printer-Release-master.zip"
TARGET_FOLDER_NAME = "G3D-Printer-Release-master"
USERNAME = "pi" #getpass.getuser()
HOME_DIR = os.path.join("/home", USERNAME) #os.path.expanduser("~")
DOWNLOADS_DIR = os.path.join(HOME_DIR, "Downloads") 
SYSTEM_CONFIG_PATH = "/boot/config.txt"
PRINTER_MODEL = read_config(SYSTEM_CONFIG_PATH, "printer_model")

if PRINTER_MODEL in ["T2000_4K", "T2000_7K", "T2000_8K", "T2000_12K"]:
    USB_MOUNT_DIR = os.path.join("/media", USERNAME)
else:
    USB_MOUNT_DIR = os.path.join("/media", "root")

UPDATE_FOLDER_DIR = os.path.join(DOWNLOADS_DIR, TARGET_FOLDER_NAME)
CURRENT_PROGRAM_DIR = os.path.join(HOME_DIR, TARGET_FOLDER_NAME)
PROGRAM_EXECUTABLE = os.path.join(HOME_DIR, TARGET_FOLDER_NAME, "build", "G3D-Printer")
CURRENT_PROGRAM_CONFIG_PATH = os.path.join(CURRENT_PROGRAM_DIR, "build", "resources", "g3d_printer.txt")
UPDATE_PROGRAM_CONFIG_PATH = os.path.join(UPDATE_FOLDER_DIR, "build", "resources", "g3d_printer.txt")
BURN_IN_FOLDER_NAME = "G3D-Burn-In-Test"
CURRENT_BURN_IN_PATH = os.path.join(HOME_DIR, BURN_IN_FOLDER_NAME)

# Variable that depends on the update file and current file.
ZIP_FILE_DIR = ""
NEW_BURN_IN_DIR = ""

# Debug messages for the paths.
print("[DEBUG]", "TARGET_FILE_NAME:" ,TARGET_FILE_NAME)
print("[DEBUG]", "TARGET_FOLDER_NAME:" ,TARGET_FOLDER_NAME)
print("[DEBUG]", "USERNAME:" ,USERNAME)
print("[DEBUG]", "HOME_DIR:" ,HOME_DIR)
print("[DEBUG]", "DOWNLOADS_DIR:" ,DOWNLOADS_DIR)
print("[DEBUG]", "USB_MOUNT_DIR:" ,USB_MOUNT_DIR)
print("[DEBUG]", "UPDATE_FOLDER_DIR:" ,UPDATE_FOLDER_DIR)
print("[DEBUG]", "ZIP_FILE_DIR:" , "To be scanned.")
print("[DEBUG]", "PROGRAM_EXECUTABLE:" , PROGRAM_EXECUTABLE)
print("[DEBUG]", "CURRENT_PROGRAM_CONFIG_PATH:" , CURRENT_PROGRAM_CONFIG_PATH)
print("[DEBUG]", "UPDATE_PROGRAM_CONFIG_PATH:" , UPDATE_PROGRAM_CONFIG_PATH)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, title_text, message_text):
        super(MainWindow, self).__init__()

        dir_path, _ =  os.path.split(sys.argv[0])
        ui_path = os.path.join(dir_path, "start_up.ui")
        loadUi(ui_path, self)

        self.title_label.setText(title_text)
        self.message_label.setText(message_text)
 
        self.no_button.clicked.connect(self.no_button_clicked)
        self.yes_button.clicked.connect(self.yes_button_clicked)
        
        self.yes_flag = 0
        self.is_busy = False
        self.is_updated = False

        self.setCursor(QtCore.Qt.BlankCursor)

        self.message_label.resize(701, 211)

    def update_message_with_delay(self, message):
        self.message_label.setText(message)
        self.repaint()
        time.sleep(2)

    def no_button_clicked(self):
        if not self.is_busy:
            self.start_program()

    def yes_button_clicked(self):
        if not self.is_busy:
            if self.yes_flag == 0:

                self.is_busy = True
                self.message_label.resize(701, 320)
                self.check_extract_update()
                self.message_label.resize(701, 211)

                QtCore.QCoreApplication.processEvents()

                self.is_busy = False
                self.yes_flag += 1

            elif self.yes_flag == 1:
                self.is_busy = True
                self.message_label.resize(701, 320)
                self.copy_update()
                self.message_label.resize(701, 211)

                QtCore.QCoreApplication.processEvents()

                self.is_busy = False
                self.yes_flag += 1

            elif self.yes_flag == 2:
                self.update_message_with_delay("Restarting printer...")
                subprocess.run(["sudo", "shutdown", "now"])
                self.yes_flag += 1

        else:
            print("Busy")

    def start_program(self):
        if not self.is_busy:
            
            if os.path.exists(PROGRAM_EXECUTABLE):
                self.update_message_with_delay("Starting program please wait...")

                result = subprocess.run(["chmod", "+x", PROGRAM_EXECUTABLE], capture_output = True)

                if result.returncode == 0:
                    print("[DEBUG] Change {} to executable success.".format(PROGRAM_EXECUTABLE))
                else:
                    print("[DEBUG] Change {} to executable fail.".format(PROGRAM_EXECUTABLE))

                current_version = self.get_software_version(CURRENT_PROGRAM_CONFIG_PATH)
                print("[DEBUG] Running program version: {}".format(current_version))
                self.hide()

                result = subprocess.run([PROGRAM_EXECUTABLE])

                if result.returncode != 0:
                    self.message_label.resize(701, 320)
                    self.title_label.setText("Error")
                    self.update_message_with_delay("Program crashed.\n\nIf you updated this previously and was interrupted,\nturn off the printer then plug a USB update to solve this.")
                    self.showFullScreen()

            else:
                self.message_label.resize(701, 320)
                self.title_label.setText("Error")
                self.update_message_with_delay("Main program cannot be found.\nTurn off the printer then plug a USB update to solve this.")
                self.showFullScreen()
                
    def check_extract_update(self):
        """
            This function checks if update file is available,
            extracts the update file in user's Downloads folder and
            extract its update version in config.
        """

        # Loop through the USB_MOUNT_DIR directory
        for dir_to_scan in os.listdir(USB_MOUNT_DIR):

            dir_to_scan_full_path = os.path.join(USB_MOUNT_DIR, dir_to_scan)

            # Double check if path exists and it is not a folder (meaning it is a file).
            if not os.path.exists(dir_to_scan_full_path) and not os.path.isdir(dir_to_scan_full_path):
                continue
            
            self.update_message_with_delay("Scanning {}".format(dir_to_scan_full_path))

            if TARGET_FILE_NAME in os.listdir(dir_to_scan_full_path):
                
                self.update_message_with_delay("Target file found.")

                # Save the directory of the zip file.
                # /media/username/usbname/G3D-Printer-Release-master.zip
                ZIP_FILE_DIR = os.path.join(dir_to_scan_full_path, TARGET_FILE_NAME)

                self.update_message_with_delay("Zip file directory: {}".format(dir_to_scan_full_path))
                
                # Extract the zip file in the user's Download's folder
                # specified by UPDATE_FOLDER_DIR.
                with zipfile.ZipFile(ZIP_FILE_DIR, "r") as zip_ref:
                    
                    # Delete existing if exists.
                    if os.path.exists(UPDATE_FOLDER_DIR):
                        self.update_message_with_delay("Deleting old update file...")
                        shutil.rmtree(UPDATE_FOLDER_DIR)

                    # Extract it.
                    zip_ref.extractall(DOWNLOADS_DIR)

                    self.update_message_with_delay("{} extracted.".format(TARGET_FILE_NAME))

                    # Get update program version
                    update_version = self.get_software_version(UPDATE_PROGRAM_CONFIG_PATH)

                    # Get current program version
                    current_version = self.get_software_version(CURRENT_PROGRAM_CONFIG_PATH)

                    update_mesage = "Current Version: {}\nUpdate Version: {}\n\nDo you want to apply the updates?".format(current_version, update_version)

                    self.update_message_with_delay(update_mesage)
                                    
                # Break if found.
                break

    def copy_update(self):
        """
            Delete the program in CURRENT_PROGRAM_DIR, copy 
            the program from UPDATE_FOLDER_DIR as new CURRENT_PROGRAM_DIR.

            This replaces the current program directory with the one from
            the USB file.
        """
        self.update_message_with_delay("Updating, please wait...")

        if os.path.exists(UPDATE_FOLDER_DIR):

            if os.path.exists(CURRENT_PROGRAM_DIR):

                self.update_message_with_delay("Deleting old program...")

                shutil.rmtree(CURRENT_PROGRAM_DIR)
            
            self.update_message_with_delay("Updating files...")

            shutil.copytree(UPDATE_FOLDER_DIR, CURRENT_PROGRAM_DIR)

            self.restore_to_default()
            
            self.update_message_with_delay("Update finished! You need to restart\nthe printer to apply the full updates.\n\nPress Yes to restart the printer.")
            
    def cloud_update_apply(self):
        self.message_label.resize(701, 320)
        self.update_message_with_delay("Applying cloud update, please wait...")

        self.showFullScreen()

        app.processEvents()

        time.sleep(5)

        app.processEvents()
    
        shutil.rmtree("/home/pi/G3D-Printer-Release-master", ignore_errors = True)

        shutil.copytree("/home/pi/Downloads/G3D-Printer-Release-master",
                        "/home/pi/G3D-Printer-Release-master")

        shutil.rmtree("/home/pi/Downloads/G3D-Printer-Release-master", ignore_errors = True)

        self.restore_to_default()
        
    def is_usb_update_present(self):
        """
            This function checks if update file is available or not.
        """

        # Loop through the USB_MOUNT_DIR directory
        for dir_to_scan in os.listdir(USB_MOUNT_DIR):

            dir_to_scan_full_path = os.path.join(USB_MOUNT_DIR, dir_to_scan)

            # Double check if path exists.
            if not os.path.exists(dir_to_scan_full_path):
                continue
            
            if TARGET_FILE_NAME in os.listdir(dir_to_scan_full_path):

                # If USB update is present, delete the downloaded cloud update.
                shutil.rmtree("/home/pi/Downloads/G3D-Printer-Release-master", ignore_errors = True)
                shutil.rmtree("/home/pi/Downloads/G3D-Printer-Release", ignore_errors = True)
                
                return True
            
        return False

    def get_software_version(self, path):

        if os.path.exists(path):
            with open(path, "r") as f:
                data = f.read()
                pattern = r"version *= *(.+)"

                return re.findall(pattern, data)
        else:
            return "NaN";

    def is_burn_in_avail(self):
        """
            This function checks if burn file folder available or not
            in the usb file path by scanning the root folder of each usb.
        """

        # Loop through the USB_MOUNT_DIR directory
        for dir_to_scan in os.listdir(USB_MOUNT_DIR):

            dir_to_scan_full_path = os.path.join(USB_MOUNT_DIR, dir_to_scan)

            # Double check if path exists and if it is not a file (meaning it is a folder).
            if not os.path.exists(dir_to_scan_full_path) and not os.path.isfile(dir_to_scan_full_path):
                continue
            
            if BURN_IN_FOLDER_NAME in os.listdir(dir_to_scan_full_path):

                global NEW_BURN_IN_DIR
                
                NEW_BURN_IN_DIR = os.path.join(dir_to_scan_full_path, BURN_IN_FOLDER_NAME)

                print("[DEBUG]", "New burn in directory detected: ", NEW_BURN_IN_DIR)

                return True
            
        return False

    def copy_burn_in(self):
        """
            This function copies the burn in folder to home folder 
            of the device. (E.g: /home/pi). If the folder already
            exists, we delete it to replace it with the new one.
        """

        if os.path.exists(CURRENT_BURN_IN_PATH):

            print("[DEBUG]", "Old burn in directory detected, deleting it...: ", CURRENT_BURN_IN_PATH)
            shutil.rmtree(CURRENT_BURN_IN_PATH)
            
        print("[DEBUG]", "Copying {} to {}".format(NEW_BURN_IN_DIR, CURRENT_BURN_IN_PATH))
        shutil.copytree(NEW_BURN_IN_DIR, CURRENT_BURN_IN_PATH)

    def run_burn_in(self):
        """
            This function simply start the python script file
            inside the burn in folder defined by the 
            variable CURRENT_BURN_IN_PATH.
        """

        script_file = os.path.join(CURRENT_BURN_IN_PATH, "burn_in_test.py")

        if os.path.exists(script_file) and os.path.isfile(script_file):

            result = subprocess.run(["chmod", "+x", script_file], capture_output = True)

            if result.returncode == 0:
                print("[DEBUG] Change {} to executable success.".format(script_file))
            else:
                print("[DEBUG] Change {} to executable fail.".format(script_file))
                
            subprocess.run(["python3", script_file])

    def restore_to_default(self):
        subprocess.run(["sudo", "python3", "/home/pi/G3D-Printer-Release-master/build/resources/scripts/reset.py"])

if __name__ == "__main__":

    # Remove the serial lock always every and
    # after burn in.
    subprocess.run(["sudo","rm", "/var/lock/LCK..ttyUSB0"])
    subprocess.run(["sudo","rm", "/var/lock/LCK..ttyUSB1"])
    subprocess.run(["sudo","rm", "/var/lock/LCK..ttyUSB2"])
    subprocess.run(["sudo","rm", "/var/lock/LCK..ttyUSB3"])
    subprocess.run(["sudo","rm", "/var/lock/LCK..ttyAMA0"])
    
    # Delay to ensure program waiting for flash drive inserted.
    time.sleep(5)

    app = QtWidgets.QApplication(sys.argv)

    # Resize to a small size to fit in first monitor then move 
    # it at 0,0 then full screen it to ensure it will 
    # full screen on the first monitor.

    title_text = "Software Update Detected"
    message_text = "A software update file has been detected\n"
    message_text += "from USB, do you want to scan its version?"
    message_text += "\nIt will not update it yet, just scan."
 
    w = MainWindow(title_text, message_text)
    w.resize(800, 480)
    w.move(0,0)
 
    
    # If burn in test file found, run it first.
    if w.is_burn_in_avail():
        w.copy_burn_in()
        w.run_burn_in()
    
    # If update file is avail, show the UI
    # so user can navigate updating.
    if w.is_usb_update_present():
        try:
            print("[DEBUG] Update file found.")
            w.showFullScreen()
        except Exception as e:
            print(str(e))
        
        
    # If cloud downloaded update is present, we replace
    # the old one in home.
    # Delete: /home/pi/G3D-Printer-Release-master
    # Copy:   /home/pi/Downloads/G3D-Printer-Release-master
    # to /home/pi
    
    elif os.path.exists("/home/pi/Downloads/G3D-Printer-Release-master"):
        try:
            w.cloud_update_apply()  
        except Exception as e:
            pass

        w.start_program()
    else:
        # Else, just start the program
        print("[DEBUG] No update file found.")
        w.start_program()

    app.exec_()
    sys.exit(0)

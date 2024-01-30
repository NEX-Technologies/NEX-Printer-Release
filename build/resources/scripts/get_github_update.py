#!/usr/bin/python3

import os
import shutil
import subprocess
import time
import sys
import requests
import glob
import urllib.request
import re
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi


repo_name = "NEX-Printer-Release-master"
repo_url = "https://github.com/NEX-Technologies/NEX-Printer-Release"
repo_nex_printer_config_url = "https://raw.githubusercontent.com/NEX-Technologies/NEX-Printer-Release/master/build/resources/nex_printer.txt"
timeout_checking_update = 30 #30 seconds
home_dir = "/home/pi/" 


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        dir_path, file_name =  os.path.split(sys.argv[0])
        ui_path = os.path.join(dir_path, "get_github_update.ui")
        
        self.update_checked = False
        self.update_started = False
        self.update_success = False

        self.update_avail = False

        print(ui_path)
        loadUi(ui_path, self)

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        self.hide_buttons(False)
        
        self.setCursor(QtCore.Qt.BlankCursor)

    def cancel_button_clicked(self):
        self.close()
    
    def continue_button_clicked(self):

        if not self.update_checked:
            self.update_checked = True
            self.hide_buttons(True)
            self.main()
            self.hide_buttons(False)
        elif self.update_avail and not self.update_started:
            self.update_started = True
            self.hide_buttons(True)
            self.update()
            self.hide_buttons(False)
        elif self.update_success:
            self.close()
            self.cancel_button.hide()
            self.continue_button.show()         
    
    def hide_buttons(self, state):
        if state:
            self.continue_button.hide()
            self.cancel_button.hide()
        else:
            self.continue_button.show()
            self.cancel_button.show()

    def is_connected(self):
        """
        This function checks if we are connected in the internet.
        We do this by simply trying to connect to a known up host,
        like https://wwww.google.com
        """

        try:
            url = "http://www.google.com"
            timeout = 10

            requests.get(url, timeout = timeout)

            print("We are connected to internet.")

            return True
            
        except Exception as exp:
            print("Error in is_connected function.")
            print(str(exp))

        return False

    def get_new_version(self):

        try:
            print("Getting new version from {}".format(repo_nex_printer_config_url))

            result = urllib.request.urlopen(repo_nex_printer_config_url, timeout = timeout_checking_update)
            contents = result.read().decode()

            pattern = r"version=([0-9\.]+)"
            match = re.search(pattern, contents)

            if match:
                major_version_num, minor_version_num, patch_num = match[1].split(".")
                
                return  major_version_num, minor_version_num, patch_num

        except Exception as exp:
            print("Error in get_new_version function.")
            print(str(exp))

        return None

    def get_current_version(self):
        
        try:
             
            current_folder = "NEX-Printer-Release-master/build/resources"
            current_update = os.path.join(home_dir, current_folder)
            full_path = os.path.join(current_update, "nex_printer.txt")

            print("Getting current version from: {}".format(full_path))

            if os.path.exists(full_path):

                with open(full_path, "r") as f:

                    contents = f.read()

                    print(contents)

                    pattern = r"version=([0-9\.]+)"
                    match = re.search(pattern, contents)

                    if match:

                        major_version_num, minor_version_num, patch_num = match[1].split(".")
                        
                        return  major_version_num, minor_version_num, patch_num
    
            
        except Exception as exp:
            print("Error in get_current_version function.")
            print(str(exp))


        print("Old version cannot be read. We download update automatically.")
        return None

    def download_update(self):
        """
        This function fetches the update from the github
        and saves it to the Downloads folder of the current user.

        If a file like that exists, we delete it first.
        """

        try:

             
            downloads_dir = os.path.join(home_dir, "Downloads")
            clone_dir = os.path.join(downloads_dir, repo_name)

            if os.path.exists(clone_dir):
                print("Previous update exists. Deleting it....")
                print("Deleting {}".format(clone_dir))
                shutil.rmtree(clone_dir)
                time.sleep(1)
                
            print("Cloning update...")
            print(repo_url)

            git_clone_process = subprocess.run(["git", "clone", repo_url, clone_dir], capture_output = True)

            if git_clone_process.returncode == 0:
                print("Successfully cloned the update.")
                print("Cloned to:", clone_dir)

                return True
            else:
                print("Cloning failed.")
        except Exception as exp:
            print("Error in download_update function.")
            print(str(exp))

        return False


    def clear_downloads(self):
        """
        This function will clear everything from
        the Downloads folder.
        """
        
        try:
             
            downloads_dir = os.path.join(home_dir, "Downloads")
            clear_downloads_dir = os.path.join(downloads_dir, "*")
            
            print("Clearing downloads folder...")
            print(clear_downloads_dir)

            command = "rm -rf {}".format(clear_downloads_dir)
            os.system(command)

            print("Downloads folder cleared.")

            return True

        except Exception as exp:
            print("Error in clear_downloads function.")
            print(str(exp))

        return False

    def update(self):
        """
        This function calls everything related to update sequence.

        returns True if update is success, False otherwise.
        """

        # if not self.is_connected():
        #     return False

        self.message_label.setText("Downloading update...\n\nThis might take up to few minutes\ndepending on your internet speed.")
        self.repaint()
        time.sleep(3)

        if not self.download_update():
            self.message_label.setText("Downloading failed, update won't\ncontinue on slow download speeds.\n\nPress cancel and start over again.")
            self.repaint()
            return False

        subprocess.run(["sudo", "python3", "/home/pi/nex-Printer-Release-master/build/resources/scripts/reset.py"])

        self.message_label.setText("Download update success!\n\nInstallation will be on next boot\nPress continue/cancel to close this window.")
        self.repaint()
        self.update_success = True

        

    def main(self):

        try:
            
            self.message_label.setText("Checking for internet connection...")
            self.repaint()
            time.sleep(3)

            if not self.is_connected():
                self.message_label.setText("Internet connection not detected.\nMake sure you're in wifi mode.\n\nPress cancel and start over again.")
                self.repaint()
                time.sleep(3)
                return False

            # Clear downloads folder since we will download new update.
            self.clear_downloads()

            current_version = self.get_current_version()
            

            if (current_version is not None):
                
                new_version = self.get_new_version()

                if new_version is not None:

                    print("Current Version: ", current_version[0], current_version[1], current_version[2])
                    print("New Version: ", new_version[0], new_version[1], new_version[2])


                    if (current_version[0] != new_version[0]) or (current_version[1] != new_version[1]) or (current_version[2] != new_version[2]):
                        self.message_label.setText("Update {}.{}.{} is available.\n\nPress continue to update.".format(new_version[0], new_version[1], new_version[2]))
                        self.repaint()
                        print("Update available.")
                        
                        self.update_avail = True

                    else:
                        self.message_label.setText("No updates available.\nPress cancel to exit.")
                        self.repaint()
                        print("No updates available.")    

            else:
                self.message_label.setText("Cannot read current version.\n\nPress continue to download update.")
                self.repaint()
                print("Cannot find current version, we auto update it.")
                self.update_avail = True


        except Exception as exp:
            self.message_label.setText("An error has occured, please update via USB instead.\n\nPress cancel to close this window.")
            self.repaint()
            print("Error fetching update. Error in function main.")
            print(str(exp))
        
    
app = QtWidgets.QApplication(sys.argv)

w = MainWindow()
w.resize(50,50)
w.move(0,0)

w.showFullScreen()

app.exec_()
 


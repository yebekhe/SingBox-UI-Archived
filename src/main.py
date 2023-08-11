from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import subprocess
import urllib.request
import os
import ctypes
import shutil
import zipfile
import configparser
import sys
import json
import time
import webbrowser
import requests
import psutil




def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
class SingBoxWindow(QMainWindow):
    def show_servers(self, _):
        # Fetching the data
        r = requests.get("http://127.0.0.1:9090/proxies", headers={"Authorization": f"Bearer YEBEKHE"})
        whole = json.loads(r.text)
        proxies = whole['proxies']

        results = []
        for key, value in proxies.items():
            if 'history' in value:
                for i in value['history']:
                    if 'delay' in i:
                        results.append((key, i['delay']))

        # Sort results by delay (which is the second item in each tuple)
        results.sort(key=lambda x: x[1])

        # Create a new window
        new_dialog = QDialog()
        new_dialog.setWindowIcon(QIcon('icon.ico'))        

        new_dialog.setGeometry(0, 0, 500, 500)

        # Add a layout to it
        layout = QVBoxLayout(new_dialog)

        # Create a QTextEdit widget and add it to the layout
        delay_text = QTextEdit(new_dialog)
        layout.addWidget(delay_text)

        # Define font properties
        bold_font = QFont()
        bold_font.setBold(True)

        for result in results:
            proxy_name, delay = result

            if delay < 600:
                color = QColor('green')
            elif 600 <= delay <= 1500:
                color = QColor('orange')
            else:
                color = QColor('red')

            delay_text.setTextColor(color)
            delay_text.setFont(bold_font)
            delay_text.append(f"{proxy_name} : {delay}")

        # Show the dialog window
        new_dialog.show()
        new_dialog.exec()
    def __init__(self):
        for proc in psutil.process_iter(['pid', 'name']):
            # TERMINATE SING-BOX.EXE IF IT IS RUNNING
            if proc.info['name'] == 'sing-box.exe':
                try:
                    process = psutil.Process(proc.info['pid']) 
                    process.terminate()  
                except psutil.NoSuchProcess:
                    print(f"No such process: {proc.info['pid']} ({proc.info['name']})")
                else:
                    print(f"Process {proc.info['pid']} ({proc.info['name']}) terminated.")
        super(SingBoxWindow, self).__init__()
        self.refresh_button = QPushButton('Refresh', self)  # Add this line
        # Create widgets
        self.label = QLabel("SUBSCRIPTION LINK: ", self)
        self.text_box = QLineEdit(self)
        self.checkbox = QCheckBox("USE LOCAL CONFIG", self)
        self.start_button = QPushButton('✅ CONNECT', self)
        self.terminate_button = QPushButton('❌ DISCONNECT', self)
        self.ip_label = QLabel("Location | IP : ", self)
        self.ip_data = QLabel(self.get_ip(), self)
        self.dashboard_button = QPushButton('📃 OPEN SING-BOX DASHBOARD', self)
        self.available_servers = QPushButton("Available Servers", self)

        # Set disable initial state for some buttons
        self.terminate_button.setEnabled(False)
        self.dashboard_button.setEnabled(False)
        self.available_servers.setEnabled(False)

        # Setup layout
        self.setupLayout()

        # Connect signals to slots
        self.start_button.clicked.connect(self.run_exe)
        self.terminate_button.clicked.connect(self.terminate_exe)
        self.dashboard_button.clicked.connect(lambda: self.open_link("http://127.0.0.1:9090/ui"))
        self.available_servers.clicked.connect(self.show_servers)
        self.refresh_button.clicked.connect(self.refresh_ip)
        # Read text from config file
        self.read_text()


    def save_text(self):
        text = self.text_box.text()
        config = configparser.ConfigParser()
        config['Text'] = {'Value': text}
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    def download_file(self):
        try:
            url = self.text_box.text()
            urllib.request.urlretrieve(url, 'config.json')
            print('File downloaded!')
        except:
            msg = QMessageBox()
            msg.setIcon(QIcon('icon.ico'))
            msg.setText("There is a problem with fetching your subscription link!\nCheck your internet connection!")
            msg.setWindowTitle("Sing-Box - YeBeKhe: ERROR!")
            msg.exec()
            return False

    def get_latest_version(self):
        command = '''powershell -Command "Invoke-WebRequest -Uri https://github.com/SagerNet/sing-box/releases/latest -UseBasicParsing | Select-Object -ExpandProperty BaseResponse | Select-Object -ExpandProperty ResponseUri | Select-Object -ExpandProperty AbsolutePath | Split-Path -Leaf"'''
        result = subprocess.check_output(command, shell=True, universal_newlines=True)    
        version = result.strip()
        return version
    def remove_files_in_dir(self, directory):
        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Create the file path
            file_path = os.path.join(directory, filename)
            # Check if the path is a file and not a directory
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)

    def run_exe(self):
        try:
            if not os.path.isfile("sing-box.exe"):
                version = self.get_latest_version()
                url="https://github.com/SagerNet/sing-box/releases/download/" + version + "/sing-box-" + version[1:] + "-windows-amd64.zip"
                output="sing-box-" + version[1:] + "-windows-amd64.zip"
                unzipped_folder="sing-box-" + version[1:] + "-windows-amd64"
                urllib.request.urlretrieve(url, output)
                destination_path = '.'
                with zipfile.ZipFile(output, 'r') as archive:
                    archive.extractall(destination_path)
                source_path = ".\\" + unzipped_folder + "\sing-box.exe"
                shutil.move(source_path, destination_path)
                os.remove(".\\" + output)
                self.remove_files_in_dir(".\\" + unzipped_folder)
                os.rmdir(".\\" + unzipped_folder)
            if self.checkbox.isChecked() == False:
                self.save_text()
                self.download_file()
            else:
                if os.path.isfile("config.json") == False:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setText("There is no Local config.json file in application folder!")
                    msg.setWindowTitle("File Not Found Error")
                    msg.setWindowTitle("Sing-Box - YeBeKhe: ERROR!")
                    msg.setWindowIcon(QIcon('icon.ico'))                
                    msg.exec()
                    return False
            process = subprocess.Popen('sing-box.exe run',creationflags=subprocess.CREATE_NO_WINDOW)
            
            print('Application running with process ID:', process.pid)
            self.start_button.setEnabled(False)
            self.terminate_button.setEnabled(True)
            self.dashboard_button.setEnabled(True)
            self.available_servers.setEnabled(True)
            time.sleep(2)
            self.change_label_text(self.ip_data, self.get_ip())
            
        except:
            msg = QMessageBox()
            msg.setIcon(QIcon('icon.ico'))
            msg.setText("There is a problem with fetching your subscription link!\nCheck your internet connection!")
            msg.setWindowTitle("Sing-Box - YeBeKhe: ERROR!")
            msg.exec()            

    def terminate_exe(self):
        for proc in psutil.process_iter(['pid', 'name']):
            # TERMINATE SING-BOX.EXE IF IT IS RUNNING
            if proc.info['name'] == 'sing-box.exe':
                try:
                    process = psutil.Process(proc.info['pid']) 
                    process.terminate()  
                except psutil.NoSuchProcess:
                    print(f"No such process: {proc.info['pid']} ({proc.info['name']})")
                else:
                    print(f"Process {proc.info['pid']} ({proc.info['name']}) terminated.")
        self.start_button.setEnabled(True)
        self.terminate_button.setEnabled(False)
        self.dashboard_button.setEnabled(False)
        self.available_servers.setEnabled(False)
        time.sleep(2)
        self.change_label_text(self.ip_data, self.get_ip())
                
    def setupLayout(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow(self.label, self.text_box)
        layout.addLayout(form_layout)

        layout.addWidget(self.checkbox)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.terminate_button)
        layout.addLayout(btn_layout)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_data)
        ip_layout.addWidget(self.refresh_button)

        layout.addLayout(ip_layout)

        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.available_servers)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def get_ip(self):
        url = "http://ip-api.com/json/"
        try:
            response = urllib.request.urlopen(url)
            if response.status == 200 :
                data = response.read()
                ip_data = json.loads(data)
                ip = ip_data['query']
                location = ip_data['country']
                return location + " | " + ip
            else:
                return "FAILED TO GET YOUR IP"
        except:
            return "FAILED TO GET YOUR IP"
    def read_text(self):
        config = configparser.ConfigParser()
        if os.path.isfile("config.ini"):
            config.read('config.ini')
            text = config.get('Text', 'Value')
            self.text_box.setText(text)

    def change_label_text(self, label, text):
        label.setText(text)

    def open_link(self, link):
        webbrowser.open(link)
    
    def refresh_ip(self):
        self.try_get_ip(3)

    def try_get_ip(self, max_attempts: int):
        for _ in range(max_attempts):
            try:
                new_ip = self.get_ip()
                self.change_label_text(self.ip_data, new_ip)
                break  # if get_ip() was successful, exit the loop
            except ConnectionResetError:
                # Sleep for a bit before trying again if there was a ConnectionResetError
                time.sleep(1)
        else:
            # If we've exhausted max_attempts and still failed to get IP,
            # then either notify user or log error as per your preference
            print("Failed to get IP after maximum number of attempts.")

class ServerDialog(QDialog):
    def __init__(self, parent=None):
        super(ServerDialog, self).__init__(parent)

        # Create widgets
        self.text_edit = QTextEdit(self)
        # Setup layout
        self.setupLayout()
        # Load data
        self.loadData()
    def setupLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
    def loadData(self):
        # Implement code here
        pass
if __name__ == "__main__":
    if is_admin():
        # The code of your tool goes here
        app = QApplication(sys.argv)
        app.setApplicationName("Sing-Box - YeBeKhe")

        window = SingBoxWindow()
        window.setWindowIcon(QIcon('icon.ico'))
        window.show()
        sys.exit(app.exec())
    else:
        # Re-run the program with admin rights, might trigger UAC prompt
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

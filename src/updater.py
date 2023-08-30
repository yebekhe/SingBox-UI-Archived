import asyncio
import os
import zipfile
import subprocess
import time
import sys 
import requests
from urllib.parse import urlparse
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QDialog
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QDialog
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtCore import QCoreApplication


class DownloadThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(Exception)

    def run(self):
        try:
            updatePrompt()
            QCoreApplication.quit()
        except Exception as e:
            self.error.emit(e)
        else:
            self.finished.emit()

def updatePrompt():
    url = "https://github.com/yebekhe/SingBox-UI/releases/latest"
    response = requests.get(url)
    
    parsed_url = urlparse(response.url)
    version = parsed_url.path.split('/')[-1]
    print(version)

    url = f"https://github.com/yebekhe/SingBox-UI/releases/download/{version}/SingboxUI.zip"

    print("Downloading the new version from ", url )
    response = requests.get(url, stream=True)

    with open("./SingboxUI.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    if os.path.exists('SingboxUI.exe'):
        try:
            os.remove('SingboxUI.exe')
            print("'SingboxUI.exe' removed successfully.")
            
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
      
    with zipfile.ZipFile('./SingboxUI.zip', 'r') as zip_ref:
        print("Extracting the new version...")
        zip_ref.extractall('./')

    DETACHED_PROCESS = 0x00000008  
    new_process = subprocess.Popen('SingboxUI.exe', creationflags=DETACHED_PROCESS)
    time.sleep(5)
    #sys.exit(0)
    os._exit(0)

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Please wait till the other app opens...", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.update_thread = DownloadThread()
        self.update_thread.finished.connect(self.finish_updating)
        self.update_thread.error.connect(self.handle_error)
        self.update_thread.start()    

    def handle_error(self, e):
        print(f"An error occurred: {e}")
        self.close() 

    def finish_updating(self):
        print("Finished updating. Exiting.")
        QCoreApplication.quit()

def run_dialog():
    app = QApplication(sys.argv)
    dialog = ProgressDialog()

    dialog.show()
    sys.exit(app.exec())

run_dialog()

import subprocess
import tkinter as tk
from tkinter import IntVar
import urllib.request
import os
import shutil
import zipfile
import configparser
import sys
import json
import time
import webbrowser

def open_link(link):
    webbrowser.open(link)

def check_state_func():
    if check_state.get() == 1:
        return True
    else:
        return False

def get_ip():
    time.sleep(5)
    url = "http://ip-api.com/json/"
    response = urllib.request.urlopen(url)
    if response.status == 200 :
        data = response.read()
        ip_data = json.loads(data)
        ip = ip_data['query']
        location = ip_data['country']
        return location + " | " + ip
    else:
        return "IP Fetch ERROR!"

def get_label_text(label):
    text = label.cget("text")
    if text is None:
        text = ""
    return text

def save_text():
    text = text_box.get()
    config = configparser.ConfigParser()
    config['Text'] = {'Value': text}
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def read_text():
    config = configparser.ConfigParser()
    if os.path.isfile("config.ini"):
        config.read('config.ini')
        text = config.get('Text', 'Value')
        text_box.insert(tk.END, text)

def change_label_text(label, text):
    label.config(text=text)

def remove_files_in_dir(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Create the file path
        file_path = os.path.join(directory, filename)
        # Check if the path is a file and not a directory
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)

def download_file():
    url = text_box.get()
    urllib.request.urlretrieve(url, 'config.json')
    print('File downloaded!')

def run_exe():
    if os.path.isfile("sing-box.exe") == False:
        version = get_latest_version()
        url="https://github.com/SagerNet/sing-box/releases/download/" + version + "/sing-box-" + version[1:] + "-windows-amd64.zip"
        output="sing-box-" + version[1:] + "-windows-amd64.zip"
        unzipped_folder="sing-box-" + version[1:] + "-windows-amd64"
        urllib.request.urlretrieve(url, output)
        destination_path = r'.'
        with zipfile.ZipFile(output, 'r') as archive:
            archive.extractall(destination_path)
        source_path = ".\\" + unzipped_folder + "\sing-box.exe"
        destination_path = r"."
        shutil.move(source_path, destination_path)
        os.remove(".\\" + output)
        remove_files_in_dir(".\\" + unzipped_folder)
        os.rmdir(".\\" + unzipped_folder)
    if check_state_func() == False:
        save_text()
        download_file()
    else:
        if os.path.isfile("config.json") == False:
            print('There is no Local config.json file in application folder!')
            return False
    process = subprocess.Popen('sing-box.exe run', creationflags=subprocess.CREATE_NO_WINDOW)
    print('Application running with process ID:', process.pid)
    start_button.config(state=tk.DISABLED)
    terminate_button.config(state=tk.NORMAL)
    dashboard_button.config(state=tk.NORMAL)
    change_label_text(ip_data, get_ip())

def terminate_exe():
    subprocess.Popen('taskkill /f /im sing-box.exe', creationflags=subprocess.CREATE_NO_WINDOW)
    print('Application terminated.')
    start_button.config(state=tk.NORMAL)
    terminate_button.config(state=tk.DISABLED)
    dashboard_button.config(state=tk.DISABLED)
    change_label_text(ip_data, get_ip())

def get_latest_version():
    command = '''powershell -Command "Invoke-WebRequest -Uri https://github.com/SagerNet/sing-box/releases/latest -UseBasicParsing | Select-Object -ExpandProperty BaseResponse | Select-Object -ExpandProperty ResponseUri | Select-Object -ExpandProperty AbsolutePath | Split-Path -Leaf"'''
    result = subprocess.check_output(command, shell=True, universal_newlines=True)    
    version = result.strip()
    return version

# Create main window
window = tk.Tk()
check_state = IntVar()
window.title('SingBox - YeBeKhe')
width = 420
height = 150
window.geometry(f"{width}x{height}")
window.resizable(False, False)
window.iconbitmap("icon.ico")

# label
label = tk.Label(window, text=" SUBSCRIPTION LINK: ")
label.grid(row=1, column=0)

# Text box
text_box = tk.Entry(window, width=33)
text_box.grid(row=1, column=1)
read_text()

#checkbox 
checkbox = tk.Checkbutton(window, text="USE LOCAL CONFIG", variable=check_state)
checkbox.grid(row=2, column=0, columnspan=2)

# Run button
start_button = tk.Button(window, text='✅ CONNECT', command=run_exe)
start_button.grid(row=3, column=0)

# Terminate button
terminate_button = tk.Button(window, text='❌ DISCONNECT', command=terminate_exe)
terminate_button.grid(row=4, column=0)
terminate_button.config(state=tk.DISABLED)

ip_label = tk.Label(window, text="Location | IP : ")
ip_label.grid(row=3, column=1)

ip_data = tk.Label(window, text=get_ip())
ip_data.grid(row=4, column=1)

dashboard_button = tk.Button(window, text='📃 OPEN SING-BOX DASHNOARD', command=lambda: open_link("http://127.0.0.1:9090/ui"))
dashboard_button.grid(row=5, column=0, columnspan=2)
dashboard_button.config(state=tk.DISABLED)

# Start the main loop
window.mainloop()

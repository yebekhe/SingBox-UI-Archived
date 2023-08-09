import subprocess
import tkinter as tk
import urllib.request
import os
import shutil
import zipfile
import configparser

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
    save_text()
    download_file()
    process = subprocess.Popen('sing-box.exe run')
    print('Application running with process ID:', process.pid)
    start_button.config(state=tk.DISABLED)
    terminate_button.config(state=tk.NORMAL)

def terminate_exe():
    os.system('taskkill /f /im sing-box.exe')
    print('Application terminated.')
    start_button.config(state=tk.NORMAL)
    terminate_button.config(state=tk.DISABLED)

def get_latest_version():
    command = '''powershell -Command "Invoke-WebRequest -Uri https://github.com/SagerNet/sing-box/releases/latest -UseBasicParsing | Select-Object -ExpandProperty BaseResponse | Select-Object -ExpandProperty ResponseUri | Select-Object -ExpandProperty AbsolutePath | Split-Path -Leaf"'''
    result = subprocess.check_output(command, shell=True, universal_newlines=True)    
    version = result.strip()
    return version

# Create main window
window = tk.Tk()
window.title('SingBox - YeBeKhe')
width = 400
height = 75
window.geometry(f"{width}x{height}")
window.resizable(False, False)
window.iconbitmap("icon.ico")

# label
label = tk.Label(window, text="Subscription Link : ")
label.grid(row=0, column=0)

# Text box
text_box = tk.Entry(window, width=33)
text_box.grid(row=0, column=1)
read_text()

# Run button
start_button = tk.Button(window, text='Connect', command=run_exe)
start_button.grid(row=1, column=0)

# Terminate button
terminate_button = tk.Button(window, text='Disconnect', command=terminate_exe)
terminate_button.grid(row=1, column=1)
terminate_button.config(state=tk.DISABLED)

# Start the main loop
window.mainloop()
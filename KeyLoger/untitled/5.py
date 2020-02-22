import numpy as np
from PIL import Image, ImageGrab, ImageOps
import cv2

while (True):
    printscreen_pil = ImageGrab.grab()
    printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8') \
        .reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
    cv2.imshow('window', printscreen_numpy)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        #        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
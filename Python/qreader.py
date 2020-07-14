import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

cam = cv2.VideoCapture(0)
cv2.namedWindow("Scanner")
img_counter = 0
qrcodes = []
while True:
    ret, frame = cam.read()
    decodedObjects = pyzbar.decode(frame)

    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Scanner", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
    for obj in decodedObjects:
    	qrcodes.append(obj.data)
    if qrcodes != []:
    	break
print(qrcodes)
cam.release()
cv2.destroyAllWindows()

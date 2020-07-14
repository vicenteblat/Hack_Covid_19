# Add necesary import statements above
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import numpy as np
from sklearn import svm
import cv2
import os
import serial
import pyzbar.pyzbar as pyzbar
import time


# Initialize firebase app
cred = credentials.Certificate("hack-covid-19-e4018-firebase-adminsdk-pt6vv-e257520af7.json")
app = firebase_admin.initialize_app(cred)
# get reference to firestore
db = firestore.client()

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

# use this function to write the result of the test to the db
# result input should be a boolean value
def write_test_result_to_db(result, test_stand_ref):
    current_test = test_stand_data["tests"][-1]  # most recent test will always be at the end of the array
    try:
        test_ref = db.collection("tests").document(current_test)
        test_ref.update({
            "result": result,
        })
        test_stand_ref.update({
            "inUse": False
        })
        return 1
    except Exception as e:
        print(e)
        return 0



def clear_leds():
    ser.write(b'B')
    ser.write(b'D')

hard_coded_stand_id = "HrPMcrft5L0k4nH6MZNC"
qrcode_data = qrcodes[0].decode("utf-8")  # unlock code obtained from scanning qrcode
print(qrcodes[0])
try:
    test_stand_ref = db.collection("test-stands").document(hard_coded_stand_id)
    test_stand_data = test_stand_ref.get().to_dict()
    print(test_stand_data["unlockCode"])
    if test_stand_data["unlockCode"] == qrcode_data:
        # functionality to run test using Alfie, and run write_test_result_to_db
        # -----------------------------------------------------------------------
        ser = serial.Serial('/dev/cu.usbmodem14601', 9600)
        clear_leds()
        cam = cv2.VideoCapture(1)
        cv2.namedWindow("test")
        while True:

            sliding_window = [0,0,0,0,0,0,1]
            k = cv2.waitKey(1)

            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 114:
                # R pressed. This resets LEDs
                clear_leds()
            # elif k%256 == 32:
                # SPACE pressed
            clear_leds()
            while sum(sliding_window) != -7 and sum(sliding_window) != 0 and sum(sliding_window) != 7:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("test", frame)
                cropped = frame[100:360, 120:520]
                edges = cv2.Canny(cropped,100,200)
                # print(edges.sum())
                if edges.sum() < 10000:
                    sliding_window.append(0)
                    sliding_window.pop(0)
                    #clear_leds()
                elif edges.sum() < 170000:
                    sliding_window.append(-1)
                    sliding_window.pop(0)
                    # print("CONGRATULATIONS! You're COVID-19 NEGATIVE")
                    # ser.write(b'C')
                    # write_test_result_to_db(False)
                    # time.sleep(4)
                    # break
                else:
                    sliding_window.append(1)
                    sliding_window.pop(0)
                    # print("We're sorry. You tested POSITIVE :(")
                    # ser.write(b'A')
                    # write_test_result_to_db(True)
                    # time.sleep(4)
                    # break
            if sliding_window[0] == -1:
                print("CONGRATULATIONS! You're COVID-19 NEGATIVE")
                ser.write(b'C')
                write_test_result_to_db(False, test_stand_ref)
                break
            elif sliding_window[0] == 1:
                print("We're sorry. You tested POSITIVE :(")
                ser.write(b'A')
                write_test_result_to_db(True, test_stand_ref)
                break
            else:
                clear_leds()

        clear_leds()
        cam.release()
        cv2.destroyAllWindows()
        # -----------------------------------------------------------------------
    else:
        print("QR Code does not correspond to this testing stand. Please try again or verify that you are using the"
              "correct stand.")
        exit()
except Exception as e:
    print(e)
    print("No such document")

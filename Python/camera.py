import numpy as np
from skimage.feature import hog
from sklearn import svm
import cv2
import os
import serial
ser = serial.Serial('/dev/cu.usbmodem14601', 9600)
ser.write(b'B')
ser.write(b'D')
# training ---------------------------------------------------------------------------
# x_train = []
# for i in range(16):
#     x_train.append(cv2.imread("positive/opencv_frame_{}.png".format(i)).flatten())
# for i in range(16):
#     x_train.append(cv2.imread("negative/opencv_frame_{}.png".format(i)).flatten())
#
# y_train = np.concatenate((np.ones(16), np.zeros(16)), axis=0)
# x_train = np.array(x_train)
# print(y_train.shape)
# print(x_train.shape)
# # mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
# classifier = svm.SVC(gamma=0.001)
# classifier.fit(x_train, y_train)
# ------------------------------------------------------------------------------------


cam = cv2.VideoCapture(1)
cv2.namedWindow("test")
img_counter = 0
# print(my_path)
# prediction = classifier.predict(np.array([cv2.imread("negative/opencv_frame_{}.png".format(i)).flatten()]))
queue = []
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    # print(k)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 114:
        ser.write(b'B')
        ser.write(b'D')
    # elif k%256 == 32:
        # SPACE pressed
    ser.write(b'B')
    ser.write(b'D')

    img_name = "opencv_frame_{}.png".format(img_counter)
    cropped = frame[100:360, 120:520]
    # save image -----------------------------------------------------
    # my_path = os.path.abspath(os.path.dirname(__file__))
    # path = os.path.join(my_path, "/negative'")
    # cv2.imwrite(os.path.join(path , img_name), cropped)
    # print("{} written!".format(img_name))
    # ----------------------------------------------------------------
    # smart prediction ----------------------------------------------
    # prediction = classifier.predict(np.array([cropped.flatten()]))
    # print(prediction)
    # if prediction[0] == 1:
    #     print("CONGRATULATIONS! You're COVID-19 NEGATIVE")
    # else:
    #     print("We're sorry. You tested POSITIVE :(")
    # ----------------------------------------------------------------
    edges = cv2.Canny(cropped,100,200)
    # print(edges.sum())
    if edges.sum() < 1000:
        ser.write(b'B')
        ser.write(b'D')
    elif edges.sum() < 190000:
        print("CONGRATULATIONS! You're COVID-19 NEGATIVE")
        ser.write(b'C')
    else:
        print("We're sorry. You tested POSITIVE :(")
        ser.write(b'A')

        # img_counter += 1

cam.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
from matplotlib import pyplot as plt

# i = 1
# img = cv2.imread("positive/opencv_frame_{}.png".format(i))
#
#
# edges = cv2.Canny(img,100,200)
#
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()

import serial                                 # add Serial library for Serial communication

Arduino_Serial = serial.Serial('/dev/cu.usbmodem14601', 9600)  #Create Serial port object called arduinoSerialData
print(Arduino_Serial.readline())               #read the serial data and print it as line
print("Enter 1 to ON LED and 0 to OFF LED")

while 1:                                      #infinite loop
    input_data = raw_input()                  #waits until user enters data
    print("you entered", input_data)           #prints the data for confirmation

    if (input_data == '1'):                   #if the entered data is 1
        Arduino_Serial.write('1')             #send 1 to arduino
        print("LED ON")


    if (input_data == '0'):                   #if the entered data is 0
        Arduino_Serial.write('0')             #send 0 to arduino
        print("LED OFF")

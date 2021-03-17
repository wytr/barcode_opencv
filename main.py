import cv2
from matplotlib import pyplot as plt
import pyzbar.pyzbar as pyzbar
import numpy as np
from itertools import cycle
import imutils
import random

#TEST branch
#---G---R---B--
#[(XXX,XXX,XXX)

colors = [(255,0,0),(255,0,255), (0,0,255),(0,255,255),(0,255,0),(255,255,0)]

colors_cycle = cycle(colors)

use_auto_rotation = False

FILEPATH = 'reel_17.jpg'
plt.rcParams['figure.figsize'] = [15, 15]


def next_color():
    return next(colors_cycle)


def draw_barcode_rect(decoded, image):
    
    color = next_color()

    (x, y, w, h) = decoded.rect
    x -= len(str(decoded.data)) * 4
    y += 10

    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),(decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),color=color,thickness=2)

    cv2.rectangle(image, (x-100, y+5), (x - 120 + len(str(decoded.data))*10 , y-15), (0,0,0), -1)               #code content field
    cv2.rectangle(image, (x-100, y+22), (x - 50 + len(str(decoded.type))*11 , y-15), (0,0,0), -1)               #code-type description field

    cv2.putText(image, str(decoded.data)[2:-1], (x - 100, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)              #code content
    cv2.putText(image, "TYPE: " + str(decoded.type), (x - 100, y+20), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)      #type description
    
    return image

def rotate(image, x):
    #image = imutils.rotate_bound(image, -1) # not cutting information off
    image = imutils.rotate(image, -x)
    return image

def decode(image):
    iteration = 1
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    
    #try to rotate the image 1 degree at a time, max 90 degrees if no code is found (timeconsuming) change use_auto_rotation to turn off
    while not decoded_objects and iteration != 90 and use_auto_rotation == True:

        temp = rotate(image, iteration)

        decoded_objects = pyzbar.decode(temp)

        iteration += 1
    

    for obj in decoded_objects:
        # draw the barcode
        print("detected barcode:", obj)
        image = draw_barcode_rect(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data)
        print()

    return image

image = cv2.imread(FILEPATH)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image = decode(image)
cv2.imwrite(FILEPATH + "_edited.png", image)
plt.imshow(image)
plt.title('scandata')
plt.show()

if __name__ == "__main__":
    from glob import glob

    barcodes = glob("barcode*.png")
    for barcode_file in barcodes:
        # load the image to opencv
        img = cv2.imread(barcode_file)
        # decode detected barcodes & get the image
        # that is drawn
        img = decode(img)
        # show the image
        cv2.imshow("img", img)
        cv2.waitKey(0)
import time
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def count_cells(image:np.array):
    # image = cv2.imread("./screens/cells.jpg")
    original = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsv_lower = np.array([156,60,0])
    hsv_upper = np.array([179,115,255])
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    minimum_area = 200
    average_cell_area = 650
    connected_cell_area = 1000
    cells = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minimum_area:
            cv2.drawContours(original, [c], -1, (36,255,12), 2)
            if area > connected_cell_area:
                cells += math.ceil(area / average_cell_area)
            else:
                cells += 1
    # print('Cells: {}'.format(cells))
    cv2.imshow('close', close)
    cv2.imshow('original', original)
    cv2.waitKey()

    return cells

def count_display_cells(image):
    original = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsv_lower = np.array([156,60,0])
    hsv_upper = np.array([179,115,255])
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    minimum_area = 200
    average_cell_area = 650
    connected_cell_area = 1000
    cells = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minimum_area:
            cv2.drawContours(original, [c], -1, (36,255,12), 2)
            if area > connected_cell_area:
                cells += math.ceil(area / average_cell_area)
            else:
                cells += 1
    print('Cells: {}'.format(cells))
    cv2.imshow('close', close)
    cv2.imshow('original', original)


def count_cells_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray, cmap='gray')
    # time.sleep(7)

    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    plt.imshow(blur, cmap='gray')
    # time.sleep(7)

    canny = cv2.Canny(blur, 30, 150, 3)
    plt.imshow(canny, cmap='gray')
    # time.sleep(7)

    dilated = cv2.dilate(canny, (1, 1), iterations=0)
    plt.imshow(dilated, cmap='gray')
    # time.sleep(7)

    (cnt, hierarchy) = cv2.findContours(
        dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    # plt.imshow(rgb)
    # time.sleep(7)

    cv2.imshow('close', rgb)
    

    print("coins in the image : ", len(cnt))


"""
# define a video capture object
vid = cv2.VideoCapture(0)

while(True):
	
    # Capture the video frame
    # by frame
    # ret, frame = vid.read()

    # Display the resulting frame
    # cv2.imshow('frame', frame)

    image = cv2.imread("./../backend/cells.jpg")
    count_display_cells(image)
    # count_cells_gray(image)
    time.sleep(5)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

# image = cv2.imread("./screens/cells.jpg")
# print(image)
# count_cells(image)
"""
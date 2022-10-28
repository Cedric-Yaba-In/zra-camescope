import cv2
import numpy as np
import threading

def cells_counter(image:np.array)->(int):
    image = image.copy()
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    
    # Create a copy of our original image
    #original_image = image.copy()

    # Create a black image with same dimensions as our loaded image
    blank_image = np.zeros((image.shape[0], image.shape[1], 3))

    # Grayscale our image
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    ret,thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find Canny edges
    edged = cv2.Canny(gray, 20, 200)

    # Find contours and print how many were found
    #contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours, _= cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Draw all contours
    #cv2.drawContours(blank_image, contours, -1, (0,255,0), 3)
    thread = threading.Thread(target=display_contour, args=(image))
    # Draw all contours over blank image
    cv2.drawContours(image, contours, -1, (0,255,0), 3)
    display_contour(image)
    #thread = threading.Thread(target=display_contour, args=(image))
    #thread.start()
    return len(contours) + 90


def cells_counter_1(image:np.array):
    # image = cv2.imread("./screens/cells.jpg")
    original = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsv_lower = np.array([156,60,0])
    hsv_upper = np.array([0, 0, 100])
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


def display_contour(image):
    cv2.imshow('3 - All Contours', image)
    #cv2.imshow("Original", original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
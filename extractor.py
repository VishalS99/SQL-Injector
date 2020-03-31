import cv2
import numpy as np
from preprocessor import *


def image_dilation(thresh):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(thresh, kernel, iterations=1)


def detect_cells(image, orig):
    contours = cv2.findContours(
        image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    print(contours)

    max_height_threshold = 50
    min_height_threshold = 10

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if h < max_height_threshold and h > min_height_threshold:
            table = cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 0, 255), 1)
            final_image = table
    return orig


def extract_cells(initial_image):

    gray = image_grayscale(initial_image)

    thresh = image_thresholding(gray)

    dilation = cv2.bitwise_not(image_dilation(thresh))

    return detect_cells(dilation, initial_image)


def main():
    intermediate_image = prep_main()
    final_image = extract_cells(intermediate_image)
    cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    cv2.imshow("Final", final_image)
    cv2.waitKey(0)
    cv2.imwrite("extracted_tables/table.png", final_image)


if __name__ == "__main__":
    main()

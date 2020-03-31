import cv2
import numpy as np


def image_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def image_blur(image):
    return cv2.bilateralFilter(image, 9, 75, 75)


def image_thresholding(image):
    return cv2.threshold(
        image, 150, 255, cv2.THRESH_BINARY_INV)[1]


def image_canny(image):
    v = np.median(image)

    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    return cv2.Canny(image, lower, upper)


def detect_rect(image):
    contours = cv2.findContours(
        image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )[:5]

    return cv2.boundingRect(contours[0])


def preprocess(initial_image):

    gray = image_grayscale(initial_image)

    blur = image_blur(gray)

    thresh = image_thresholding(blur)

    canny = image_canny(thresh)

    return canny


def prep_main():

    initial_image = cv2.imread("./images/image.png")
    preprocessed = preprocess(initial_image)

    [x, y, w, h] = detect_rect(preprocessed)

    final_image = initial_image[y-5:y+h+5, x-5:x+w+5]

    return final_image

# if __name__ == "__main__":
#     prep_main()

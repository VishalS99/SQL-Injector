import cv2
import numpy as np


def image_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def image_blur(image):
    return cv2.GaussianBlur(image, (3, 3), cv2.BORDER_DEFAULT)


def image_dilation(thresh):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(thresh, kernel, iterations=1)


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

    thresh = image_dilation(thresh)

    print("## Cropped image and saved")
    cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    cv2.imshow("Final", thresh)

    canny = image_canny(thresh)
    print("## Cropped image and saved")
    cv2.namedWindow("fa", cv2.WINDOW_NORMAL)
    cv2.imshow("fa", canny)
    return canny


# def prep_main():

    # initial_image = cv2.imread("./images/table2.png")

    # initial_image = cv2.copyMakeBorder(
    #     initial_image, 20, 20, 20, 20, cv2.BORDER_CONSTANT, (0, 0, 0))

    # preprocessed = preprocess(initial_image)

    # [x, y, w, h] = detect_rect(preprocessed)

    # final_image = initial_image[y-5:y+h+5, x-5:x+w+5]
    # print("## Cropped image and saved")
    # cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    # cv2.imshow("Final", final_image)

    # cv2.waitKey(0)

    # return final_image


# if __name__ == "__main__":
#     prep_main()

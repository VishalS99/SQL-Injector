import cv2
import numpy as np
from preprocessor import *

table_headings = []
table_row_elements = []

try:
    import pytesseract
except:
    print("Cannot import Tesseract")


def sort_contours(cnts, method="left-to-right"):

    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)


def image_dilation(thresh):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(thresh, kernel, iterations=1)


def detect_cells(image, orig):
    contours = cv2.findContours(
        image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    contours, boundingBoxes = sort_contours(contours, "top-to-bottom")
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]

    box = []

    max_height_threshold = 80
    min_height_threshold = 22

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if h < max_height_threshold and h > min_height_threshold and w < 300:
            table = cv2.rectangle(
                orig, (x-2, y-2), (x+w+2, y+h+2), (0, 0, 255), 1)
            box.append([x, y, w, h])
            final_image = table
    return (orig, box)


def extract_cell_loc(image, box):
    global table_headings, table_row_elements

    countcol = 0
    countrow = 0
    rowval = box[0][1]
    colval = box[0][0]
    for i in range(len(box)):
        if box[i][1] != rowval:
            break
        else:
            countcol += 1
    countrow = int(len(box) / countcol)

    print("### Detection of table titles")
    for i in range(countcol):
        (x, y, w, h) = box[i]
        text_image = image[y: y+h, x: x+w]
        text_image = cv2.resize(text_image, None, fx=2, fy=2,
                                interpolation=cv2.INTER_CUBIC)
        resizing = image_grayscale(text_image)
        text = pytesseract.image_to_string(resizing)
        if(len(text) == 0):
            out = pytesseract.image_to_string(
                resizing, config='--psm 3')

        table_headings.append(text.replace("\n", ' '))
    table_headings.reverse()
    print("=======> Heading Entry:", table_headings, "\n")

    print("### Detection of table entries")
    for i in range(1, countrow):
        row_entry = []
        for j in range(countcol):
            (x, y, w, h) = box[countcol*i + j]
            text_image = image[y: y+h, x: x+w]

            text_image = cv2.resize(text_image, None, fx=2, fy=2,
                                    interpolation=cv2.INTER_CUBIC)
            resizing = image_grayscale(text_image)
            # resizing = cv2.threshold(
            #     text_image, 180, 255,  cv2.THRESH_BINARY)[1]
            # resizing = cv2.medianBlur(resizing, 3)

            text = pytesseract.image_to_string(resizing)
            if(len(text) == 0):
                text = pytesseract.image_to_string(
                    resizing, config='--psm 3')

            row_entry.append(text.replace("\n", ' '))
        row_entry.reverse()
        print("=======> Row Entry: ", row_entry, "\n")
        table_row_elements.append(row_entry)

    return (table_headings, table_row_elements)


def extract_cells(initial_image):

    gray = image_grayscale(initial_image)

    thresh = image_thresholding(gray)

    dilation = cv2.bitwise_not(image_dilation(thresh))

    return detect_cells(dilation, initial_image)


def main():
    # initial_image = prep_main()
    initial_image = cv2.imread("./images/tt.jpg")
    if initial_image.shape[1] > 640 and initial_image.shape[0] > 640:
        scale_percent = 40  # percent of original size
        width = int(initial_image.shape[1] * scale_percent / 100)
        height = int(initial_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        initial_image = cv2.resize(
            initial_image, dim, interpolation=cv2.INTER_AREA)

    print("## Initial preprocessing of the image")
    print("## Extraction of table - Detection of cells")
    final_image, box_data = extract_cells(initial_image)
    cv2.imwrite("extracted_tables/table.png", final_image)

    print("## Extraction of table - Extraction of cell data")
    headings, row_entries = extract_cell_loc(final_image, box_data)

    print("## Saving data in Table_data.txt")
    open("Table_data.txt", "w").close()
    table_data = open("Table_data.txt", "a")
    table_data.write("HEADING: \n")
    for i in range(len(headings)):
        table_data.write(headings[i] + "\t")
    table_data.write("\n")
    for i in range(len(row_entries)):
        for j in range(len(row_entries[i])):
            table_data.write(row_entries[i][j] + "\t")
        table_data.write("\n")

    table_data.close()


if __name__ == "__main__":
    main()

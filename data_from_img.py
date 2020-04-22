from PIL import Image
import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# NICD_Updates-21-04-2020.jpg

def get_tot_data(img_path):
    img_cv = cv2.imread(img_path)
    orig_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # coords in form of [x0,x1,y0,y1]
    tot_stats_coords = dict(
        unknown=[190, 190 + 100, 134, 128 + 32],
        confirmed=[280, 280 + 100, 170, 170 + 32],
        tests=[271, 271 + 121, 210, 210 + 32],
        deaths=[165, 165 + 100, 247, 247 + 32],
    )

    def getSubImg(coord_key):
        coords = tot_stats_coords[coord_key]
        sub_img = orig_img[coords[2]:coords[3], coords[0]:coords[1]]
        return sub_img

    def preprocess_img(in_img):
        gray_img = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY)
        ret, thresh_img = cv2.threshold(np.array(gray_img), 125, 255, cv2.THRESH_BINARY)
        inv_img = cv2.bitwise_not(thresh_img)
        return inv_img

    def no_from_img(dict_key):
        sub_proc_img = preprocess_img(getSubImg(dict_key))
        return pytesseract.image_to_string(sub_proc_img, config='--psm 7 digits')

    print("Unkown: " + no_from_img('unknown'))
    print("Confirmed Cases: " + no_from_img('confirmed'))
    print("Tests Conducted: " + no_from_img('tests'))
    print("Deaths: " + no_from_img('deaths'))

    # print(no_from_img("Unknown: " + no_from_img('unknown')))
    # print(no_from_img("Confirmed Cases: " + no_from_img('confirmed')))
    # print(no_from_img("Tests Conducted: " + no_from_img('tests')))
    # print(no_from_img("Deaths: " + no_from_img('deaths')))


get_tot_data(r'NICD updates/NICD_Updates-21-04-2020.jpg')

from PIL import Image
import pytesseract
import cv2
from matplotlib import pyplot as plt
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Will most likely move these to a JSON file later on for ease of use
prov_death_coords = {
    'ec': [226, 78, 368, 31],
    'fs': [226, 78, 404, 31],
    'gp': [226, 78, 440, 31],
    'kzn': [226, 78, 474, 31],
    'lp': [226, 78, 510, 31],
    'mp': [226, 78, 549, 31],
    'nw': [226, 78, 587, 31],
    'nc': [226, 78, 625, 31],
    'wc': [226, 78, 665, 31]
}

prov_recovered_coords = {
    'ec': [308, 78, 368, 31],
    'fs': [308, 78, 404, 31],
    'gp': [308, 78, 440, 31],
    'kzn': [308, 78, 474, 31],
    'lp': [308, 78, 510, 31],
    'mp': [308, 78, 549, 31],
    'nw': [308, 78, 587, 31],
    'nc': [308, 78, 625, 31],
    'wc': [308, 78, 665, 31]
}

prov_confirmed_coords = dict(
    # Easier ways to get these but while I'm here...
    gp = [695, 93, 303, 28],
    kzn = [1120, 112, 547, 32],
    nw = [765, 65, 430, 31],
    lp = [918, 68, 312, 30],
    mp = [1112, 52, 383, 33],
    fs = [814, 58, 529, 28],
    wc = [585, 66, 744, 25],
    ec = [805, 79, 689, 29]
)

gen_tot_coords = dict(
    unknown = [190,100,134,32],
    confirmed = [280, 100, 170, 32],
    tests = [271, 121, 210, 32],
    deaths = [165, 100, 247, 32],
)

date_coords=[557, 210 , 116, 45]


def get_tot_data(img_path):
    img_cv = cv2.imread(img_path)
    orig_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    dimensions = (1280, 905)
    orig_img = cv2.resize(orig_img, dimensions)

    # pre-processing
    img_arr = np.array(orig_img)
    red, green, blue = img_arr.T
    threshold = 150
    white_areas = (red > threshold) & (blue > threshold) & (green > threshold)
    img_arr[..., :][white_areas.T] = (0, 0, 0)
    convert_img = np.where(img_arr == 0, 0, 255)
    convert_img = convert_img.astype(np.uint8)

    img = convert_img

    def get_sub_img(coords):
        sub_img = img[coords[2]:coords[2] + coords[3], coords[0]:coords[0] + coords[1]]
        return sub_img

    def preprocess_img(in_img):
        proc_img = in_img
        ret, prc_img = cv2.threshold(np.array(proc_img), 125, 255, cv2.THRESH_BINARY)
        proc_img = cv2.blur(proc_img, (2, 2))
        return proc_img

    def no_from_img(coords, preprocess=False, show_img=False):
        # sub_proc_img = preprocess_img(getSubImg(dict_key))
        sub_proc_img = get_sub_img(coords)
        if (preprocess):
            sub_proc_img = preprocess_img(sub_proc_img)
        if (show_img):
            plt.imshow(sub_proc_img)
            plt.show()
        return pytesseract.image_to_string(sub_proc_img, config='--psm 7 digits')

    date = no_from_img(date_coords)

    print("Date done")
    prov_deaths_totals = dict()
    prov_recovered_totals = dict()
    prov_confirmed_totals = dict()

    for coords in prov_death_coords:
        amount = no_from_img(prov_death_coords[coords], True)
        prov_deaths_totals[coords.upper()] = amount

    print("prov_death_totals done")

    for coords in prov_recovered_coords:
        amount = no_from_img(prov_recovered_coords[coords], True)
        prov_recovered_totals[coords.upper()] = amount

    print("prov_recovered_totals done")

    # for coords in prov_confirmed_coords:
    #     amount = no_from_img(prov_confirmed_coords[coords], True)
    #     prov_confirmed_totals[coords.upper()] = amount
    #     print(coords.upper() + " done")

    # print("")
    #
    # print("prov_confirmed_totals done")

    gen_totals = dict(
        unknown=no_from_img(gen_tot_coords['unknown']),
        confirmed=no_from_img(gen_tot_coords['confirmed']),
        tests=no_from_img(gen_tot_coords['tests']),
        deaths=no_from_img(gen_tot_coords['deaths']),

    )

    print("gen_totals done")

    return date, prov_deaths_totals, prov_recovered_totals, gen_totals

# prov_confirmed_totals

# img_path = "NICD_updates/NICD_Updates_04_21.jpg"
# date, prov_deaths_totals, prov_recovered_totals, prov_confirmed_totals, gen_totals = get_tot_data(img_path)
# print("Image Path: " + img_path)
# print("Date: " + date)
# print("Deaths:", prov_deaths_totals)
# print("Recovered: ", prov_recovered_totals)
# print("Confirmed: ", prov_confirmed_totals)
# print("General: ", gen_totals)

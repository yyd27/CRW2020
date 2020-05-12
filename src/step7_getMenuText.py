import os, re, glob
import textract
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

fpath = './menu_folder/'
tpath = "./menu_text/"
tmpimgpath = "./menu_tmpimg/"
dirs = glob.glob(fpath + "*")

ocr_ids = [187, 270, 117, 427, 426, 349, 330, 329, 197, 198, 166, 283, 1,
           18, 112, 126, 128, 149, 152, 170, 177, 185, 188, 200, 231, 232, 242,
           244, 260, 273, 286, 290, 295, 311, 313, 314, 315, 316, 317, 318,
           328, 334, 335, 337, 347, 353, 356, 359, 362, 385, 386, 411,
           416, 434, 435, 436, 437, 438]

for d in dirs:
    ind = d.replace(fpath, "")
    pdfs = glob.glob(d + '/*.pdf')
    if int(ind) in ocr_ids:
        # Use OCR:
        for pi,p in enumerate(pdfs):
            pages = convert_from_path(p)
            text2 = ""
            for ipage, page in enumerate(pages):
                tmp_page = tmpimgpath + "_".join([str(ind), str(pi), str(ipage)]) + ".jpg"
                page.save(tmp_page, "JPEG")
                imgtext = str(((pytesseract.image_to_string(Image.open(tmp_page)))))
                text2 = text2 + imgtext + '\n'

            with open(tpath + str(ind) + '_' + str(pi) + ".txt", "w") as wf:
                wf.write(text2)
    else:
        ## Use textextract:
        for pi,p in enumerate(pdfs):
            text = textract.process(p)
            text2 = text.decode('utf-8')

            with open(tpath + str(ind) + '_' + str(pi) + ".txt", "w") as wf:
                wf.write(text2)
                


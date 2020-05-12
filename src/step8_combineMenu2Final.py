import pandas as pd
import numpy as np
import re, os, glob
import json
import matplotlib.pyplot as plt
import seaborn as sns

with open("final_data.txt") as rf1:
    fdic = json.load(rf1)

# read in menu text
fpath = "./menu_text/"

#re_price = re.compile(r"\$\d\d")
#re_price2 = re.compile(r"\d\d\.00")
#re_price3 = re.compile(r"\d{2}\s+per\s+person")

cnt = 0
for k in fdic.keys():
    menufn = glob.glob(fpath + str(k) + "_*.txt")
    menu_text = []
    for f in menufn:
        text = open(f,encoding = "utf-8").read()
        # get $
##        price = re_price.findall(text)
##        
##        if (len(price) == 0) or ((len(price) > 1) and (price[0] not in ["$24", "$36", "$48"])):           
##            price2 = re_price3.findall(text)
##            if len(price2) == 0:
##                print(f)
##                cnt += 1
##            elif len(price2) > 0:
##                tmp = price2[0]
##                if re.findall("\d{2}",tmp)[0] not in ["24","36","48"]:
##                    print(f)
##                    cnt += 1
        # get dinner/lunch
        if "dinner" in text.lower() and "lunch" in text.lower():
            print(f)
            cnt += 1
        
        menu_text.append(text)

    fdic[k]['menu_text'] = menu_text

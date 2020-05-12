from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, random, re, os
from bs4 import BeautifulSoup
import pandas as pd
import json

# webdriver setup
driverLocation = '/usr/local/bin/chromedriver'

# read href
with open("menu_hrefs.txt") as rf:
    menu_dict = json.load(rf)

# download
Rkeys = list(menu_dict.keys()) #["3"]
for Rkey in Rkeys:
    pdflist = menu_dict[Rkey]
    if len(pdflist) > 0:
        Rdir = "/Users/username/menu_folder/" + str(Rkey) + "/"
        if not os.path.exists(Rdir):
            os.makedirs(Rdir)

        options = Options()
        options.add_experimental_option("prefs", {
          "download.default_directory": Rdir,
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True,
          "plugins.always_open_pdf_externally": True
        })

        driver = webdriver.Chrome(driverLocation, chrome_options = options)

        try:
            for purl in pdflist:
                driver.get(purl)
                time.sleep(2)
                
            time.sleep(20)
        finally:
            driver.quit()
    


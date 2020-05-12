from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time,random
from bs4 import BeautifulSoup
import pandas as pd
import json

driverLocation = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(driverLocation)

# read detail data
dfindex = pd.read_csv("Rindex.txt", sep = "|", encoding = 'utf-8')

href_dict = {}
bad_i = []

for i,row in dfindex.iterrows():
    time.sleep(random.randint(1, 5))
    
    tmpurl = row['url']
    driver.get(tmpurl)
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[text()="View menu"]').click()

    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'crwMenuModal'))
        )
        # get href    
        innerHTML = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(innerHTML,'html.parser')

        tar_divs = soup.findAll('div', attrs={"style":"right:0;bottom:0"})
        hrefs = []
        for tar in tar_divs:
            hrefs.append(tar.find('a')['href'])

        href_dict[i] = hrefs
    except:
        print("---Menu failed for %d" % i)
        print(tmpurl)
        bad_i.append(i)
        
#finally:
#    driver.quit()

href_dict2 = {str(k):href_dict[k] for k in href_dict}
with open('menu_hrefs.txt', 'w') as wf:
    json.dump(href_dict2, wf)

### not useful in this case but great to learn (it's clicking sth. under newly pop-up modal):
#jscommand = driver.find_element(By.XPATH, '//a[text()="Find a table"]')
#jscommand = driver.find_element(By.XPATH, '//button[text()="View menu"]')
#driver.execute_script("arguments[0].click();", jscommand)



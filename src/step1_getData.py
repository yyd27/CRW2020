from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import json

def getData():
    baseurl = 'https://www.choosechicago.com/chicago-restaurant-week/participating-restaurants/'
    driverLocation = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(driverLocation)

    pages_postfix = [""] + ["?pg=" + str(i) for i in range(2, 10)]
    isFirstTime  = True
    Rdict = {}
    rid = 0

    for ipage, page in enumerate(pages_postfix):
        pageurl = baseurl + page
        driver.get(pageurl)
        time.sleep(60)
        
        if isFirstTime:
            driver.find_element_by_xpath('//button[@data-dismiss="alert"]').click()
            time.sleep(2)
            isFirstTime = False

        innerHTML = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(innerHTML,'html.parser')

        # get Rlist
        Rlist = soup.findAll('div', attrs={"class":"card-body"})
        Rlist = [r for r in Rlist if len(r.text.strip()) > 0]

        for iR, R in enumerate(Rlist):
            ## cuisines
            tmp = R.find('h6', attrs={"class":"card-subtitle"})
            cuisines = [s.text.strip() for s in tmp.findAll('span')]
            ## name
            tmp = R.find('h5')
            name = tmp.text.strip()
            detail_url = tmp.find('a')['href']
            ## address
            tmp = R.find('p')
            address = tmp.text.strip()
            ## gluten/vegetarian & lunch/dinner options
            tmp_gv, tmp_bld = R.findAll('ul')
            # gluteen/vege
            gv0 = tmp_gv.findAll("li")
            gv1 = [i.find("img") for i in gv0]
            gv = [i["alt"] for i in gv1 if i is not None]
            # brunch/lunch/dinner
            bld0 = tmp_bld.findAll("li")
            bld = [i.text.strip() for i in bld0]

            ## save
            Rdict[rid] = {'page': ipage + 1, 'pg_id': iR + 1,
                          'name': name, 'cuisines': cuisines,
                          'address': address, 'url': detail_url,
                          'alt_option': gv, 'meal_option': bld}
            rid += 1
            
    # save as dataframe
    Rdf = pd.DataFrame.from_dict(Rdict, orient = 'index')
    Rdf.to_csv("Rindex.txt", sep = "|", encoding = 'utf-8', index=False)
    
if __name__ == '__main__':
    getData()

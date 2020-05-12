from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import pandas as pd
import json
import step1_getData 

def getDetails():
    step1_getData.getData()

    dfindex = pd.read_csv("Rindex.txt", sep = "|", encoding = 'utf-8')

    dfindex['neighbor'] = "unknown"
    dfindex['des'] = "unknown"

    driverLocation = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(driverLocation)
    
    # create a directory to save details
    if not os.path.exists("./Details/"):
        os.makedirs("./Details/")
        
    for i,row in dfindex.iterrows():
        if i % 100 == 0:
            print("Crawling %d th restaurants..." % i)
        tmpurl = row['url']
        
        driver.get(tmpurl)
        content = driver.page_source
        time.sleep(5)
        soup = BeautifulSoup(content, "html.parser")

        # get neighbor
        pn = soup.find("p", attrs = {"class": "font-weight-semi-bold text-muted mb-md-0"})
        neighbor = pn.text.strip()
        dfindex.at[i, 'neighbor'] = neighbor

        # get description
        pdes0 = content.split('class="mb-5 small">')[0]
        pdes1 = pdes0.split('</div></div>')[-1]
        pdessoup = BeautifulSoup(pdes1, "html.parser")
        des = " ".join([p.text.strip() for p in pdessoup.findAll("p")])

        dfindex.at[i, 'des'] = des
        
        # get capacities etc.
        fid = 0
        fdict = {}
        sections = content.split('<span class="col">')
        for sec in sections:
            sec_name = sec.split('</span>')[0]
            rows = sec.split('<p class="mb-0 py-2 row border-top border-light">')
            if len(rows) == 1:
                continue
            else:
                spanrows = rows[1:]

                for spanrow in spanrows:
                    rowsoup = BeautifulSoup(spanrow, "html.parser")
                    fspan = rowsoup.find("span", attrs = {"class": "font-weight-light col-9 col-sm-5 col-md-8"}) 
                    vspan = rowsoup.find("span", attrs = {"class": "col-3 col-sm-7 col-md-4"})

                    if fspan != None and vspan != None:
                        fdict[fid] = {'section': sec_name,
                                      'feature': fspan.text.strip(),
                                      'value': vspan.text.strip(),
                                      }
                        fid += 1
		tdf = pd.DataFrame.from_dict(fdict,orient='index')
		tdf.to_csv("./Details/" + str(i) + ".txt",
				   sep = "|", encoding = 'utf-8', index = False)

    dfindex.to_csv("Rindex_w_des.txt", sep = "|", encoding = 'utf-8', index=False)

if __name__ == '__main__':
    getDetails()

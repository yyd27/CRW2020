import pandas as pd
import numpy as np
import re, os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import step3_getYelp

def combineWebYelp():
    API_Key = input("Enter your Yelp API key: ")
    step3_getYelp.getYelp(API_Key)
    
    ### combine yelp data & restaurant week data
    # read data in
    dfindex = pd.read_csv("Rindex_w_des.txt", sep = "|", encoding = 'utf-8')
    dfindex['ind'] = dfindex.index

    with open("yelp_best_match_json.txt") as rf1:
        dy1 = json.load(rf1)

    dfyelp = pd.DataFrame.from_dict(dy1, orient = 'index')
    dfyelp['ind'] = dfyelp.index
    dfyelp['ind'] = dfyelp['ind'].astype(int)

    # join
    df = pd.merge(dfindex, dfyelp, how = "left", on = ['ind']).fillna("unknown")

    # check the whether the match is successful by matching name & address
    df['ratio_name'] = df.apply(lambda row: fuzz.ratio(str(row['name']).lower(), str(row['Yname']).lower()), axis = 1)

    df['Yaddress1'] = "unknown"
    for i,row in df.iterrows():
        tmp = row['Yaddress']
        if tmp != "unknown":
            df.at[i, 'Yaddress1'] = tmp['address1']

    df['ratio_address'] = df.apply(lambda row: fuzz.ratio(str(row['address']).lower(), str(row['Yaddress1']).lower()), axis = 1)

    ### manually check restaurants that don't match
    ##tmp = df.loc[(df['ratio_address'] <= 50) & (df['ratio_name'] <= 50)]
    ##
    ### manual modification
    ##codict = {165: {'name': 'Hoyts'}, # Hoyt’s Modern American Tavern
    ## 306: {'name': 'Rock Bottom Restaurant & Brewery'}, # Rock Bottom Restaurant & Brewery – Downtown Chicago
    ## 362: {'name': 'TAO Chicago Restaurant'} # TAO
    ## }

    dfdict = df.to_dict(orient = 'index')
    dfdict2 = {str(k):dfdict[k] for k in dfdict}
    with open('final_data.txt', 'w') as wf:
        json.dump(dfdict2, wf)

if __name__ == '__main__':
    combineWebYelp()
    



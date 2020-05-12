import pandas as pd
import numpy as np
import re, os
import requests,json
import time
import json
import step2_getDetails

def getYelp(API_Key):
    def PickRyelp(Rname, Raddress, biz_list):
        best_biz_id = 0
        max_name_ratio = 0
        max_address_ratio = 0
        
        for i, biz in enumerate(biz_list):
            biz_name = biz['name']
            biz_address = biz['location']['address1']
            name_ratio = fuzz.ratio(str(Rname).lower(), str(biz_name).lower())
            address_ratio = fuzz.ratio(str(Raddress).lower(), str(biz_address).lower())

            if name_ratio > max_name_ratio or address_ratio > max_address_ratio:
                if name_ratio + address_ratio > max_name_ratio + max_address_ratio:
                    best_biz_id = i
                    max_name_ratio = name_ratio
                    max_address_ratio = address_ratio
                    
        return(biz_list[best_biz_id])

    url_params = {}
    api_key = API_Key
    headers = {'Authorization': 'Bearer %s' % api_key,}

    baseurl = "https://api.yelp.com/v3/businesses/search"

    ### read data in
    step2_getDetails.getDetails()
    dfindex = pd.read_csv("Rindex_w_des.txt", sep = "|", encoding = 'utf-8')

    correction_dict = {165: {'name': 'Hoyts'}, # Hoyt’s Modern American Tavern
     306: {'name': 'Rock Bottom Restaurant & Brewery'}, # Rock Bottom Restaurant & Brewery – Downtown Chicago
     362: {'name': 'TAO Chicago Restaurant'} # TAO
     }

    ### get yelp
    yelpdict = {}
    for i,row in dfindex.iterrows():
        ### get response
        if i not in correction_dict.keys():
            Rname = str(row['name'])
            Rname = re.sub(r"[!#$%&\'()*+,-./:;<=>?@^_`{|}~]+", " ", Rname)
            Rname = Rname.replace("CheSa’s at ","")
            Rname = Rname.replace("’", " ")
        else:
            Rname = correction_dict[i]['name']

        Rname_text = "-".join(Rname.lower().split(' '))
        
        Raddress = str(row['address'])

        url = baseurl + "?term=" + Rname_text + "&location=chicago"
        response = requests.request('GET', url, headers=headers, params=url_params)
        result_json = response.json()
        b = result_json['businesses']

        if len(b) > 0:
            Ryelp = PickRyelp(Rname, Raddress, b)

            if 'name' in Ryelp.keys():
                yname = Ryelp['name']
            else:
                yname = "unknown"

            if 'location' in Ryelp.keys():
                yaddress = Ryelp['location']
            else:
                yaddress = "unknown"

            if 'price' in Ryelp.keys():
                price = Ryelp['price']
            else:
                price = "unknown"

            if 'rating' in Ryelp.keys():
                rating = Ryelp['rating']
            else:
                rating = -1

            if 'coordinates' in Ryelp.keys():
                coordinates = Ryelp['coordinates']
            else:
                coordinates = {"latitude": 0, "longitude": 0}

            if 'review_count' in Ryelp.keys():
                review_count = Ryelp['review_count']
            else:
                review_count = -1

            yelpdict[i] = {
                'Yname': yname,
                'Yaddress': yaddress,
                'price': price,
                'rating': rating,
                'coordinates': coordinates,
                'review_count': review_count}
        else: # no match in yelp
            yelpdict[i] = {
                'Yname': "unknown",
                'Yaddress': "unknown",
                'price': "unknown",
                'rating': -1,
                'coordinates': {"latitude": 0, "longitude": 0},
                'review_count': -1}
            
        time.sleep(0.5)

    yelpdict2 = {str(k):yelpdict[k] for k in yelpdict}
    with open('yelp_best_match_json.txt', 'w') as wf:
        json.dump(yelpdict2, wf)
        
if __name__ == '__main__':
    API_Key = input("Enter your Yelp API key: ")
    getYelp(API_Key)


import json
import os
import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
import numpy as np
import pandas as pd

base_url = "https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All{}"

leanings = {}
for page in ['', '&page=1', '&page=2']:
    url = base_url.format(page)

    while True:
        try:
            html = urlopen(url)
            break
        except URLError:
            time.sleep(1)

    soup = BeautifulSoup(html, "lxml")
    
    for row in soup.findAll('tr', {'class': 'even'}):
        site = row.contents[1].find('a')['href'].split('/')[-1]
        leaning = row.contents[3].find('a')['href'].split('/')[-1]
        leanings[site] = leaning

    for row in soup.findAll('tr', {'class': 'odd'}):
        site = row.contents[1].find('a')['href'].split('/')[-1]
        leaning = row.contents[3].find('a')['href'].split('/')[-1]
        leanings[site] = leaning 

leaning_df = pd.DataFrame.from_dict(leanings, orient='index').reset_index()
leaning_df.to_csv('derived_data/media_classification/allsides_raw.csv', index=False)

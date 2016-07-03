from lxml import html
import requests
import pandas as pd
import re, urllib
from bs4 import BeautifulSoup

MAIN_URL_L = ["http://www.3dprintingdatabase.org/en/3dmaterials/en/3dmaterials?field_technology_value=All&field_generic_material_value=All&field_materials_value=All&items_per_page=250",
            "http://www.3dprintingdatabase.org/en/3dmaterials/en/3dmaterials?field_technology_value=All&field_generic_material_value=All&field_materials_value=All&items_per_page=250&page=1",
            "http://www.3dprintingdatabase.org/en/3dmaterials/en/3dmaterials?field_technology_value=All&field_generic_material_value=All&field_materials_value=All&items_per_page=250&page=2",
          ]
#url = 'http://www.3dprintingdatabase.org/en/3dmaterials/shell-200-series-0'


def get_child_urls():
    l = []
    for MAIN_URL in MAIN_URL_L:
        for i in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(MAIN_URL).read(), re.I):
            if '/en/3dmaterials/' in i and '?' not in i:
                l.append(i)
            try:
                for ee in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(i).read(), re.I):

                    if '/en/3dmaterials/' not in ee:
                        continue
                    if '?' in ee:
                        continue
                    l.append(ee)
            except:
                pass
                #print "problem ", i

    l = list(set(l))
    return l



def get_page_data(url):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    myTH = soup.findAll('th')
    myTD = soup.findAll('td')
    data_d = {}
    name = url.split("/")[-1]
    data_d.update({'name': name})
    for i in range(len(myTH)):
        key = myTH[i].text.encode('utf-8').strip()
        val = myTD[i].text.encode('utf-8').strip()
        data_d.update({key: val})

    df = pd\
        .DataFrame(data_d.items())\
        .rename(columns = {0: 'parameter',
                           1: name + '_value'})
    return df


print "Getting urls..."
urls = get_child_urls()
N_urls = len(urls)


CHILD_URL_PREFIX = 'http://www.3dprintingdatabase.org'

print "Getting urls data..."
df_l = []
ctr = 0

##for url in urls[:5]:
for url in urls:
    # print some progress report
    ctr += 1
    print "scan item ", ctr, " out of ", N_urls, "items"

    # add the prefix
    url = CHILD_URL_PREFIX + url

    try:
        dfi = get_page_data(url)
        df_l.append(dfi)
    except:
        print "problem with url ", url

tmp_df = df_l[0]
for ii in range(1, len(df_l)):
    try:
        tmp_df = pd.merge(tmp_df, df_l[ii], on='parameter', how='outer')
    except:
        pass

# and now Transpose it
tmp_df_T = tmp_df.T
header_prev = tmp_df_T.columns.values
header_next = tmp_df_T[0:1].values[0]
header_d ={}
for i in range(len(header_prev)):
    header_d.update({header_prev[i]: header_next[i]})
tmp_df_T = tmp_df_T.rename(columns=header_d)
tmp_df_T = tmp_df_T.ix[1:]

# save it in csv
tmp_df_T.to_csv('3dprintingdatabase.csv')

import ipdb;ipdb.set_trace()
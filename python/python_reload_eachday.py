import pandas as pd
import numpy as np
import requests
import sys
import os
import json
import datetime
def join_df_bykey(leftdf,rightdf, leftkey,rightkey):
    newdf = leftdf.join(rightdf.set_index(rightkey), on=leftkey, how='left', lsuffix='_left', rsuffix='_right')
    return newdf
dir_path = os.path.dirname(os.path.realpath(__file__))
# If not same date with marker, the data needs to reload from server
todaydateStr = datetime.date.today().strftime("20%y-%m-%d")
current_date_marker = open('{0}/date_updated_marker.txt'.format(dir_path),'r').read()
print('start download')
url = 'https://aqicn.org/data-platform/covid19/report/10806-5622c73e/2020'
myfile = requests.get(url)

open('{0}/waqi-covid-2020.csv'.format(dir_path), 'wb').write(myfile.content)
print('Down load is finished')
csv2020_aqi = '{0}/waqi-covid-2020.csv'.format(dir_path)
csv2019_aqi = '{0}/waqi-covid19-airqualitydata-2019.csv'.format(dir_path)
csvcountry_alpha2 = '{0}/country-alpha2-code.csv'.format(dir_path)
df_2020 = pd.read_csv(csv2020_aqi,comment='#')
df_2019 = pd.read_csv(csv2019_aqi,comment='#')
country_alpha2 = pd.read_csv(csvcountry_alpha2,comment='#')
print('Start joint')
df_2020_fullc = join_df_bykey(df_2020, country_alpha2, 'Country','alpha-2-code')
print('Start append')
df_2020_2019_fullc = df_2020_fullc.append(df_2019,ignore_index=True)
print('Start csv 2020_2019')
df_2020_2019_fullc.to_csv('waqi-covid19-airqualitydata-2020_2019.csv',index=False)
open('{0}/date_updated_marker.txt'.format(dir_path),'w').write(todaydateStr)

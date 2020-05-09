import pandas as pd
import numpy as np
import requests
import sys
import os
import json
import datetime
dir_path = os.path.dirname(os.path.realpath(__file__))
# # If not same date with marker, the data needs to reload from server
# todaydateStr = datetime.date.today().strftime("20%y-%m-%d")
# current_date_marker = open('{0}/date_updated_marker.txt'.format(dir_path),'r').read()
# if current_date_marker != todaydateStr:
#     url = 'https://aqicn.org/data-platform/covid19/report/10806-5622c73e/2020'
#     myfile = requests.get(url)
#     open('{0}/waqi-covid-2020.csv'.format(dir_path), 'wb').write(myfile.content)
#     open('{0}/date_updated_marker.txt'.format(dir_path),'w').write(todaydateStr)




csv2019q1_aqi = '{0}/waqi-covid19-airqualitydata-2019Q1.csv'.format(dir_path)
csv2019q2_aqi = '{0}/waqi-covid19-airqualitydata-2019Q2.csv'.format(dir_path)
csv2019q3_aqi = '{0}/waqi-covid19-airqualitydata-2019Q3.csv'.format(dir_path)
csv2019q4_aqi = '{0}/waqi-covid19-airqualitydata-2019Q4.csv'.format(dir_path)
csvcountry_alpha2 = '{0}/country-alpha2-code.csv'.format(dir_path)
# df_2020 = pd.read_csv(csv2020_aqi,comment='#')
df_2019_q1 = pd.read_csv(csv2019q1_aqi,comment='#')
df_2019_q2 = pd.read_csv(csv2019q2_aqi,comment='#')
df_2019_q3 = pd.read_csv(csv2019q3_aqi,comment='#')
df_2019_q4 = pd.read_csv(csv2019q4_aqi,comment='#')
alldf = []
alldf.append(df_2019_q1)
alldf.append(df_2019_q2)
alldf.append(df_2019_q3)
alldf.append(df_2019_q4)
country_alpha2 = pd.read_csv(csvcountry_alpha2,comment='#')

df_2019_fullc = []

def join_df_bykey(leftdf,rightdf, leftkey,rightkey):
    newdf = leftdf.join(rightdf.set_index(rightkey), on=leftkey, how='left', lsuffix='_left', rsuffix='_right')
    return newdf

x_1 = join_df_bykey(df_2019_q1, country_alpha2, 'Country','alpha-2-code')
x_2 = join_df_bykey(df_2019_q2, country_alpha2, 'Country','alpha-2-code')
x_3 = join_df_bykey(df_2019_q3, country_alpha2, 'Country','alpha-2-code')
x_4 = join_df_bykey(df_2019_q4, country_alpha2, 'Country','alpha-2-code')
# for x_df in alldf:
#     re_df = join_df_bykey(x_df, country_alpha2, 'Country','alpha-2-code')
#     df_2019_fullc.append(re_df)
    # truedf=truedf.append(re_df,ignore_index=True)

# truedf.to_csv('waqi-covid19-airqualitydata-2019.csv',index=False)
x = x_1.append(x_2,ignore_index=True).append(x_3,ignore_index=True).append(x_4,ignore_index=True)
x.to_csv('waqi-covid19-airqualitydata-2019.csv',index=False)

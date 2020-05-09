import pandas as pd
import numpy as np
import requests
import sys
import os
import json

# url = 'https://aqicn.org/data-platform/covid19/report/10806-5622c73e/2020'
# myfile = requests.get(url)
# open('waqi-covid-2020.csv', 'wb').write(myfile.content)
dir_path = os.path.dirname(os.path.realpath(__file__))

csv2020_aqi = '{0}/waqi-covid-2020.csv'.format(dir_path)
csv2019q1_aqi = '{0}/waqi-covid19-airqualitydata-2019Q1.csv'.format(dir_path)
csv2019q2_aqi = '{0}/waqi-covid19-airqualitydata-2019Q2.csv'.format(dir_path)
csv2019q3_aqi = '{0}/waqi-covid19-airqualitydata-2019Q3.csv'.format(dir_path)
csv2019q4_aqi = '{0}/waqi-covid19-airqualitydata-2019Q4.csv'.format(dir_path)
csvcountry_alpha2 = '{0}/country-alpha2-code.csv'.format(dir_path)
df_2020 = pd.read_csv(csv2020_aqi,comment='#')
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


def join_df_bykey(leftdf,rightdf, leftkey,rightkey):
    newdf = leftdf.join(rightdf.set_index(rightkey), on=leftkey, how='left', lsuffix='_left', rsuffix='_right')
    return newdf
# country_1 = "Australia"
# city_1 = "Sydney"
# pollutant_1 = "no2"
# country_1 = sys.argv[1]
# city_1 = sys.argv[2]
# pollutant_1 = sys.argv[3]
df_2020_fullc = join_df_bykey(df_2020, country_alpha2, 'Country','alpha-2-code')
for x_df in alldf:
    re_df = join_df_bykey(x_df, country_alpha2, 'Country','alpha-2-code')
    df_2020_fullc=df_2020_fullc.append(re_df,ignore_index=True)
output = {}

uniq_countries = df_2020_fullc.Country_right.unique()
for country in uniq_countries:
    uniq_cities = df_2020_fullc.loc[df_2020_fullc['Country_right'] == country].City.unique()
    output.update({country:{}})
    for city in uniq_cities:
        uniq_pollutants = df_2020_fullc.loc[(df_2020_fullc['Country_right'] == country) & (df_2020_fullc['City'] == city)].Specie.unique()
        output[country].update({city:[]})
        for pollutant in uniq_pollutants:
            output[country][city].append(pollutant)

#df_selected = df_2020_fullc.loc[(df_2020_fullc['Country_right'] == country_1) & (df_2020_fullc['City'] == city_1) &(df_2020_fullc['Specie'] == pollutant_1)].sort_values(by=['Date'],ascending=True)
#website provide country, city (optional),pollutant,year(optional),  value : average 
#and df_2020_fullc['City'] == city_1
# df_selected.sort_values(by=['Date'],ascending=False,inplace=True)
# df_selected.to_csv('./user_requested_data/{0}_{1}_{2}.csv'.format(country_1,city_1,pollutant_1))
# df_res = df_selected[['Date','Country_right','City','Specie','median']]
# output = {
#     'date':'',
#     'median': ''
# }
# output['date'] = df_res['Date'].to_list()
# output['median'] = df_res['median'].to_list()
# # output_string = '{date:{0},value:{1}}'.format(df_res['Date'].values,df_res['median'].values)
#output_string = json.dumps(output)

# print(output_string)
with open('country_city.json', 'w') as outfile:
    json.dump(output, outfile)
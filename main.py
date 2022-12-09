from src import getdata, savedata
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import seaborn as sns

english_dict = {'발전량':'Power Generation',
                '일조합(hr)':'Time of sunshine(hr)',
                '일조율(%)':'Percentage of sunshine(%)',
                '일사합(MJ/m2)':'Amount of sunshine(MJ/m2)',
                '평균기온(℃)':'Average Temperature(℃)',
                '최고기온(℃)':'Maximum Temperature(℃)',
                '최저기온(℃)':'Minimum Temperature(℃)',
                '평균습도(%rh)':'Average Humid(%rh)',
                '최저습도(%rh)':'Minmum Humid(%rh)',
                '강수량(mm)':'Precipitation(mm)'}

def grouping(df):
    #make data frame grouped by date, power generation
    droped_df = df.drop(['day', '1시간최다강수량(mm)'], axis=1)
    groupedby_month_year = droped_df.groupby(['year','month'])
    groupedby_pg = droped_df.drop(['year','month'], axis=1)\
                               .groupby(df[english_dict['발전량']]
                               #grouping power generation by 100 unit
                               .apply(lambda x: round(x, 1)//100)) 
    return groupedby_month_year, groupedby_pg

if __name__ == "__main__":
    getdata.set_font()
    df = getdata.get_data(True)
    df.rename(columns = english_dict, inplace=True)

    df_groupedby_month_year, df_groupedby_pg = grouping(df)
   
    

    

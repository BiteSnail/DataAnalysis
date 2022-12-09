from src import getdata, savedata
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import seaborn as sns

english_dict = {'발전량':'PowerGeneration',
                '일조합(hr)':'Timeofsunshine(hr)',
                '일조율(%)':'Percentageofsunshine(%)',
                '일사합(MJ/m2)':'Amountofsunshine(MJ/m2)',
                '평균기온(℃)':'AverageTemperature(℃)',
                '최고기온(℃)':'MaximumTemperature(℃)',
                '최저기온(℃)':'MinimumTemperature(℃)',
                '평균습도(%rh)':'AverageHumid(%rh)',
                '최저습도(%rh)':'MinmumHumid(%rh)',
                '강수량(mm)':'Precipitation(mm)'}

image_path = '.\\result\\images\\'

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

    savedata.save_csv_result(df_groupedby_month_year, df_groupedby_pg)
    savedata.save_images_result(df_groupedby_month_year.median(), df)




   
    

    

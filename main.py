from src import getdata, savedata
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

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

def make_csv_result(df_groupedby_month_year, df_groupedby_pg):
    powermedian = df_groupedby_month_year.median()
    indexmedian = powermedian.reset_index()
    powermean = df_groupedby_pg.mean()
    
    pp = powermedian.pivot('year', 'month', english_dict['발전량'])
    for i in range(2019, 2023, 1):
        savedata.save_data(powermedian.xs(i, level='year').corr(), 'corr'+str(i))
    savedata.save_data(pp, 'tablepowermax')
    savedata.save_data(powermedian.corr(), 'corr')
    savedata.save_data(indexmedian, 'median')
    savedata.save_data(powermean, 'mean')

def make_images_result(l):
    #make bar plot
    l.plot(kind='bar', y=english_dict['발전량'])
    plt.title('Monthly solar power median')
    plt.ylabel('amount of solar power')
    plt.xlabel('year-month')
    plt.savefig(image_path+'Monthly solar power median.png')

    #make heatmap plot
    colormap = plt.cm.PuBu
    plt.figure(figsize=(10, 8))
    plt.title("Power Generation Correlation of Climate", y = 1.05, size = 15)
    sns.heatmap(l.astype(float).corr(), linewidths = 0.1, vmax = 1.0,
            square = True, cmap = colormap, linecolor = "white", annot = True, annot_kws = {"size" : 16})
    plt.savefig(image_path+'Power Generation Correlation of Climate.png')

    #make 3 columns data frame
    solar_power = {english_dict['일조합(hr)']:list(l.reset_index()[english_dict['일조합(hr)']]), 
                english_dict['일사합(MJ/m2)']:list(l.reset_index()[english_dict['일사합(MJ/m2)']]),
                english_dict['발전량']:list(l.reset_index()[english_dict['발전량']])}
    deviation = pd.DataFrame(solar_power)

    #make scatter plot
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(deviation['일조합(hr)'], deviation['일사합(MJ/m2)'],deviation['발전량'], marker='o', s=15, cmap='Greens')
    plt.title('Scatter of Power Gneration')
    plt.ylabel('amount of sunshine')
    plt.xlabel('hours of sunshine')
    plt.savefig(image_path+'Scatter of Power Gneration')

if __name__ == "__main__":
    getdata.set_font()
    df = getdata.get_data(True)
    df.rename(columns = english_dict, inplace=True)

    df_groupedby_month_year, df_groupedby_pg = grouping(df)

    make_csv_result(df_groupedby_month_year, df_groupedby_pg)
    make_images_result(df_groupedby_month_year.median())


   
    

    

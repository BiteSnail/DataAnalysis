import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

image_path = '.\\result\\images\\'
saved_path = ".\\result\\"
file_prefix_name = "\\files\\"
file_format = ".csv"
english_dict = {'발전량':'PowerGeneration',
                '일조합(hr)':'Timeofsunshine(hr)',
                '일조율(%)':'Percentageofsunshine(%)',
                '일사합(MJ/m2)':'Amountofsunshine(MJ_m2)',
                '평균기온(℃)':'AverageTemperature(℃)',
                '최고기온(℃)':'MaximumTemperature(℃)',
                '최저기온(℃)':'MinimumTemperature(℃)',
                '평균습도(%rh)':'AverageHumid(%rh)',
                '최저습도(%rh)':'MinmumHumid(%rh)',
                '강수량(mm)':'Precipitation(mm)'}


def save_data(data, file_name="", encoding="utf-8-sig"):
    data.to_csv(saved_path+file_prefix_name+file_name+file_format,encoding=encoding)
    return

def save_csv_result(df_groupedby_month_year, df_groupedby_pg):
    powermedian = df_groupedby_month_year.median()
    indexmedian = powermedian.reset_index()
    powermean = df_groupedby_pg.mean()
    
    pp = indexmedian.pivot('year', 'month', english_dict['발전량'])
    for i in range(2019, 2023, 1):
        save_data(powermedian.xs(i, level='year').corr(), 'corr'+str(i))
    save_data(pp, 'tablepowermax')
    save_data(powermedian.corr(), 'corr')
    save_data(indexmedian, 'median')
    save_data(powermean, 'mean')

def save_images_result(l, df=pd.DataFrame()):
    #make bar plot
    l.plot(kind='bar', y=english_dict['발전량'])
    plt.title('Monthly solar power median')
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylabel('amount of solar power')
    plt.xlabel('year-month')
    plt.savefig(image_path+'Monthly solar power median.png')

    #make heatmap plot
    colormap = plt.cm.PuBu
    plt.figure(figsize=(10, 8))
    plt.rcParams['axes.unicode_minus'] = False
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
    plt.rcParams['axes.unicode_minus'] = False
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(deviation[english_dict['일조합(hr)']], \
                deviation[english_dict['일사합(MJ/m2)']],
                deviation[english_dict['발전량']], 
                marker='o', s=15, cmap='Greens')
    plt.title('Scatter of Power Gneration')
    plt.ylabel('amount of sunshine')
    plt.xlabel('hours of sunshine')
    plt.savefig(image_path+'Scatter of Power Gneration.png')

    #make every plot
    sns.pairplot(df[df.PowerGeneration < 5000].drop(['month', 'year', 'day'], axis=1))
    plt.rcParams['axes.unicode_minus'] = False
    plt.savefig(image_path+'All relatioin.png')
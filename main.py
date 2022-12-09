from src import getdata, savedata, predictdata
import pandas as pd
import matplotlib.pyplot as plt

def grouping(df):
    #make data frame grouped by date, power generation
    droped_df = df.drop(['day', '1시간최다강수량(mm)'], axis=1)
    groupedby_month_year = droped_df.groupby(['year','month'])
    groupedby_pg = droped_df.drop(['year','month'], axis=1)\
                               .groupby(df[savedata.english_dict['발전량']]
                               #grouping power generation by 100 unit
                               .apply(lambda x: round(x, 1)//100)) 
    return groupedby_month_year, groupedby_pg

if __name__ == "__main__":
    print('===<program start>===')
    getdata.set_font()
    print('Complete Loading Font')
    df = getdata.get_data(True)
    print('Complete Loading Data')
    df.rename(columns = savedata.english_dict, inplace=True)
    print('Complete translate column name korean to english')

    df_groupedby_month_year, df_groupedby_pg = grouping(df)

    savedata.save_csv_result(df_groupedby_month_year, df_groupedby_pg)
    print('Complete save csv')
    savedata.save_images_result(df_groupedby_month_year.median(), df)
    print('Complete save plot image')

    x, y = predictdata.preprocess(df)
    pr, x_train, x_test, y_train, y_test = predictdata.get_predictmodel(x, y)
    MSE, RMSE = predictdata.pridict(pr, x, y)
    print('MSE: ', MSE)
    print('RMSE: ', RMSE)
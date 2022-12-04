import os, json
import pandas as pd

configpath = "\\src\\common\\config.json"
powergeneration_key = "power_generation_data"
name_list = "name_list"
datafile_dir = 'datafile_dir'
drop_cols = ['분당', '청주', '양산']
rename_col = {'수원' : '발전량'}
start_date = '2019-09-01'
end_date = '2022-03-31'
date_col_name = ('일시', '실적일자')
place_col_name = '지점명'

def get_data_filename_list():
    # return config path data list
    with open(os.getcwd() + configpath, 'r', encoding="UTF-8") as json_file:
        file_list = json.load(json_file)
    return file_list

def get_data(merged=False):
    # return data from csvs
    file_list = get_data_filename_list()
    data_list = {}
    merged_df = pd.DataFrame()

    for key, file_name in file_list[name_list].items():
        data_list[key] = pd.read_csv(file_list[datafile_dir]+file_name).fillna(0)
        #태양광 발전량의 경우 수원만 남기고 다 삭제
        if key == powergeneration_key:
            data_list[key] = data_list[key].drop(drop_cols, axis=1)\
                                            .rename(columns=rename_col)
            data_list[key][date_col_name[1]] = pd.to_datetime(data_list[key][date_col_name[1]])
            merged_df['year'] = data_list[key][date_col_name[1]].dt.year
            merged_df['month'] = data_list[key][date_col_name[1]].dt.month
            merged_df['day'] = data_list[key][date_col_name[1]].dt.day
            merged_df = pd.concat([merged_df, data_list[key].iloc[:,1:]], axis=1)
        #날씨 정보의 경우 2019-09-01이상인 것으로 필터링
        else:
            temp_data = data_list[key][date_col_name[0]]
            mask = (start_date <= temp_data) & (temp_data <= end_date)
            data_list[key] = data_list[key][mask].reset_index(drop=True)
            merged_df = pd.concat([merged_df, data_list[key].drop([date_col_name[0], place_col_name], axis=1)],axis=1)

    if merged == True:
        return merged_df
    else:
        return data_list
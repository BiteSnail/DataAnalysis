import os
import pandas as pd

saved_path = ".\\result\\"
file_prefix_name = "test"
file_format = ".csv"

def save_data(data, file_name="", encoding="utf-8-sig"):
    data.to_csv(saved_path+file_prefix_name+file_name+file_format,encoding=encoding)
    return
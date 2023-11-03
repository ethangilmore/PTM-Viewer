import os
import re
import pandas as pd

MOD_COLUMN = 'modification_info'
MOD_PATTERN = r'-?\d+\.\d+'

def read_file(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.tsv'):
        return pd.read_csv(file_path, sep='\t')
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise Exception(f'Invalid file type: {os.path.splitext(file_path)[1]}')

def read_files(file_paths):
    combined_df = pd.DataFrame()
    for file_path in file_paths:
        df = read_file(file_path)
        try:
            combined_df = pd.concat([combined_df, df])
        except:
            raise Exception(f'Selected files have mismatching columns and cannot be combined')
    return combined_df

def get_modifications(df):
    if MOD_COLUMN not in df.columns:
        raise Exception(f'For detection of modifications, files must contain a "{MOD_COLUMN}" column')
    
    modification_info = df[MOD_COLUMN].dropna().unique().tolist()
    modifications = {}
    for modifications_string in modification_info:
        for modification in re.findall(MOD_PATTERN, modifications_string):
            if modification not in modifications:
                modifications[modification] = 0
            modifications[modification] += 1
    
    return list(modifications.keys()), list(modifications.values())

def filter_by_modifications(df, modifications):
    filtered_df = pd.DataFrame()
    for modification in modifications:
        filtered_df = pd.concat([filtered_df, df[df[MOD_COLUMN].str.contains(modification, na=False)]])
    return filtered_df
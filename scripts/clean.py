import pandas as pd
import numpy as np
from .preprocess import preprocess

# Func to perform mean imputation
def mean_imputation(series):
    return series.fillna(series.mean().round(2)) 

# Func to perform median imputation
def median_imputation(series):
    return series.fillna(series.median())
    
# Func to clears data frame removing rows with null values
def clear_data_frame(df):
    return df.dropna()

def convert_column_to_int(df, column):
    df[column] = df[column].astype(int)
    return df

def final_clear_df(df, column = 'ano'):
    df = preprocess(df)
    df = clear_data_frame(df)
    df = convert_column_to_int(df, column)
    return df
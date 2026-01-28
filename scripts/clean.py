import pandas as pd
import numpy as np

# Func to perform mean imputation
def mean_imputation(series):
    return series.fillna(series.mean().round(2)) 

# Func to perform median imputation
def median_imputation(series):
    return series.fillna(series.median())
    
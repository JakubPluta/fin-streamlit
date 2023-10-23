import pandas as pd
import numpy as np


def clean_data(data, labels: list):
    data.drop(labels, inplace=True)
    cols = data.select_dtypes(exclude="int").columns.to_list()
    data[cols] = data[cols].astype("str")
    data = data.replace(["None", "0", 0], np.nan).dropna(how="all")
    return data


def _prepare_statement_df(data: dict):
    df = pd.json_normalize(data).T
    df.columns = df.iloc[0]
    df = df[1:]
    return df

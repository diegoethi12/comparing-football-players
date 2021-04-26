
import re
import pandas as pd

from src import SRC_PATH
from src.utils.files import read_pickle


def rename_unnamed_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    return df.rename(columns=lambda x: re.sub(r'Unnamed:.*', 'General', x))


def flatten_multiindex_columns(columns: list) -> list:
    return [' - '.join(col).strip() for col in columns]


def concat_columns(dataframe: pd.DataFrame, columns: str) -> pd.DataFrame:
    return dataframe[columns].apply(lambda row: ' - '.join(row.values.astype(str)), axis=1)


dfs_dict = read_pickle(SRC_PATH / 'data' / 'metrics-dict-2021-04-22.pickle')
keys = ['General - Player', 'General - Nation', 'General - Squad']

for k, df in dfs_dict.items():
    dfs_dict[k] = rename_unnamed_columns(df)
    dfs_dict[k].columns = flatten_multiindex_columns(dfs_dict[k].columns.values)
    dfs_dict[k] = dfs_dict[k].query('`General - Player` != "Player"')
    dfs_dict[k].index = concat_columns(dfs_dict[k], keys)


pd.concat(dfs_dict.values(), axis=1)

import re
import pandas as pd
from pathlib import PosixPath
import logging

from src import SRC_PATH
from src.utils.files import read_pickle
from src.utils.dates import today_str


def rename_unnamed_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    return df.rename(columns=lambda x: re.sub(r'Unnamed:.*', 'General', x))


def flatten_multiindex_columns(columns: list) -> list:
    return [' - '.join(col).strip() for col in columns]


def concat_columns(dataframe: pd.DataFrame, columns: str) -> pd.DataFrame:
    return dataframe[columns].apply(lambda row: ' - '.join(row.values.astype(str)), axis=1)


def merge_data(path: PosixPath, columns: list) -> PosixPath:
    dfs_dict = read_pickle(path)

    for k, df in dfs_dict.items():
        logging.info(f"Formatting {k} dataframe")
        dfs_dict[k] = rename_unnamed_columns(df)
        dfs_dict[k].columns = flatten_multiindex_columns(dfs_dict[k].columns.values)
        dfs_dict[k] = dfs_dict[k].query('`General - Player` != "Player"')
        dfs_dict[k].index = concat_columns(dfs_dict[k], columns)

    logging.info(f"Merging dataframes on: {', '.join(columns)}")
    df = pd.concat(dfs_dict.values(), axis=1)
    file_name = f"players-df-{today_str('%Y-%m-%d')}.pickle"
    file_path = SRC_PATH / 'data' / file_name
    df.to_pickle(file_path)

    return file_path


if __name__ == '__main__':
    merge_data(
        path=SRC_PATH / 'data' / 'metrics-dict-2019-2020-big5-2021-05-04.pickle',
        columns=['General - Player', 'General - Nation', 'General - Squad']
    )

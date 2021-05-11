import numpy as np
import pandas as pd
import logging
from pathlib import PosixPath

from src import DATA_PATH
from src.utils.files import read_pickle
from src.utils.dates import today_str


def delete_duplicated_columns_by_nulls(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Sort columns by # of nulls and deduplicate
    :param dataframe:
    :return:
    """
    df = dataframe.copy()
    nulls = df.isna().sum()
    indexes = np.arange(0, len(df.columns))
    idx_nulls = pd.DataFrame({"index": indexes, "col": df.columns.values, "null": nulls})
    selected_columns = idx_nulls.sort_values('null', ascending=True).drop_duplicates('col', keep='first')['index'].values
    return df.iloc[:, selected_columns]


def delete_goalkeepers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Delete Goalkeepers
    :param dataframe:
    :return:
    """
    df = dataframe.copy()
    deleted_rows = len(df.query('`General - Pos` in ["GK"]'))
    logging.info(f"Deleting {deleted_rows} rows of goalkeepers")
    return df.query('`General - Pos` not in ["GK"]')


def clean_substitute_players(dataframe: pd.DataFrame, min_played_time_ratio: float) -> pd.DataFrame:
    """
    Filter player by played games using a ratio
    :param dataframe:
    :param min_played_time_ratio:
    :return:
    """
    df = dataframe.copy()
    df['Playing Time - MP'] = df['Playing Time - MP'].astype(float)
    min_played_games = round(np.max(df['Playing Time - MP']) * min_played_time_ratio, 1)
    logging.info(
        f"Deleting {len(df[df['Playing Time - MP'] <= min_played_games])} players "
        f"that played less than {min_played_games} games."
    )
    return df[df['Playing Time - MP'] > min_played_games]


def remove_nulls_columns(dataframe: pd.DataFrame, nulls_ratio: float) -> pd.DataFrame:
    """
    Delete nulls columns
    :param dataframe:
    :param nulls_ratio:
    :return:
    """
    df = dataframe.copy()
    not_na_columns = list(df.columns[(df.isna().sum() < len(df)*nulls_ratio)])
    logging.info(f"Deleting {len(df.columns)-len(not_na_columns)} columns that have more "
                 f"than {round(len(df)*nulls_ratio)} nulls values"
                 )
    return df[not_na_columns]


def clean_data(path: PosixPath, min_played_time_ratio, nulls_ratio):
    """
    All cleaning process
    :param path:
    :param min_played_time_ratio:
    :param nulls_ratio:
    :return:
    """
    # Read and clean dataframe
    df = read_pickle(path)
    logging.info(f"Initial shape of the dataframe: {df.shape}")
    df = delete_duplicated_columns_by_nulls(df)
    df = delete_goalkeepers(df)
    df = clean_substitute_players(df, min_played_time_ratio)
    df = remove_nulls_columns(df, nulls_ratio)
    logging.info(f"Final shape of the dataframe: {df.shape}")

    # Save dataframe
    file_name = f"cleaned-df-{today_str('%Y-%m-%d')}.pickle"
    logging.info(f"Saving dataframe on {DATA_PATH / file_name}")
    df.to_pickle(DATA_PATH / file_name)


if __name__ == '__main__':
    clean_data(DATA_PATH / 'players-df-2021-05-04.pickle', 0.1, 0.5)

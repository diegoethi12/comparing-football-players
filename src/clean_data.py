import plotly.express as px
import numpy as np
import pandas as pd
import logging

from src import DATA_PATH
from src.utils.files import read_pickle
from src.utils.dates import today_str

df = read_pickle(DATA_PATH / 'players-df-2021-05-04.pickle')

# Sort columns by # of nulls and deduplicate
nulls = df.isna().sum()
indexes = np.arange(0, len(df.columns))
idx_nulls = pd.DataFrame({"index": indexes, "col": df.columns.values, "null": nulls})
selected_columns = idx_nulls.sort_values('null', ascending=True).drop_duplicates('col', keep='first')['index'].values
df = df.iloc[:, selected_columns]

# Delete Goalkeepers
df['General - Pos'].unique()
deleted_rows = len(df.query('`General - Pos` in ["GK"]'))
logging.info(f"Deleting {deleted_rows} rows of goalkeepers")
df = df.query('`General - Pos` not in ["GK"]')

# Filter player by played games (10%)
df['Playing Time - MP'] = df['Playing Time - MP'].astype(float)
px.histogram(df['Playing Time - MP']).show()
min_played_games = np.max(df['Playing Time - MP']) / 10
logging.info(
    f"Deleting {len(df[df['Playing Time - MP'] <= min_played_games])} players "
    f"that played less than {min_played_games} games."
)
df = df[df['Playing Time - MP'] > min_played_games]

# Delete nulls columns
not_na_columns = list(df.columns[(df.isna().sum() < len(df)/2)])
logging.info(f"Deleting {len(df.columns)-len(not_na_columns)} columns that have more than {len(df)/2} nulls values")
df = df[not_na_columns]

file_name = f"cleaned-df-{today_str('%Y-%m-%d')}.pickle"
df.to_pickle(DATA_PATH / file_name)

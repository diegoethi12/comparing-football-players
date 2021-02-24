import pandas as pd
from datetime import datetime
import pickle
import logging

from src import SRC_PATH
from src.utils.files import read_yaml


def read_html_and_log(url: str) -> pd.DataFrame:
    df = pd.read_html(url)[0]
    logging.info(f"Processing url {url}")
    return df


if __name__ == '__main__':
    logging.info("Reading links file")
    links = read_yaml(SRC_PATH / 'links.yaml')
    dfs = {key: read_html_and_log(link) for key, link in links['big5'][2020].items()}

    file_name = f"metrics-dict-{datetime.utcnow().strftime('%Y-%m-%d')}"

    with open(f'{file_name}.pickle', 'wb') as handle:
        pickle.dump(dfs, handle, protocol=pickle.HIGHEST_PROTOCOL)

import pandas as pd
from datetime import datetime
import pickle
import logging
from pathlib import PosixPath

from src import SRC_PATH
from src.utils.files import read_yaml


def read_html_and_log(url: str) -> pd.DataFrame:
    df = pd.read_html(url)[0]
    logging.info(f"Processing url {url}")
    return df


def get_data(links_file: PosixPath) -> None:
    logging.info("Reading links file")
    links = read_yaml(SRC_PATH / links_file)

    data_path = SRC_PATH / 'data'
    data_path.mkdir(exist_ok=True)

    dfs = {key: read_html_and_log(link) for key, link in links['big5'][2020].items()}

    file_name = f"metrics-dict-{datetime.utcnow().strftime('%Y-%m-%d')}"

    with open(f'{data_path}/{file_name}.pickle', 'wb') as handle:
        pickle.dump(dfs, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    get_data('links.yaml')

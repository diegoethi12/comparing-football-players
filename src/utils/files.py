from pathlib import PosixPath
from typing import Any
import yaml
import pickle


def read_yaml(path: PosixPath) -> dict:
    with open(path) as file:
        yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_dict


def read_pickle(path: PosixPath) -> Any:
    with open(path, 'rb') as file:
        output = pickle.load(file)
    return output

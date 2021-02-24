import yaml


def read_yaml(path: str) -> dict:
    with open(path) as file:
        yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_dict

import yaml

def load_config(file_path='/home/idea/code/sqlib_v2/config_handler/config.yaml'):
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def check_config(config, key, subkey):
    try:
        value = config[key][subkey]
        print(f"{key}.{subkey} found in config.")
        return value
    except KeyError:
        raise KeyError(f"Key '{subkey}' not found under '{key}' in config.")
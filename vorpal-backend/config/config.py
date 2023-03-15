import yaml
import os

CONFIG_FILE = 'config.yaml'
CONFIG_TEMPLATE_FILE = 'config_template.yaml'
CONFIG_TEMPLATE = {
    'media': {
        'directory': '/path/to/media',
        'extensions': ['.mp3', '.m4a', '.flac', '.ogg', '.wav', '.mp4']
    },
    'cache': {
        'maxsize': 1024,
        'ttl': 2592000 # 1 month
    }
}

def create_template_config():
    with open(CONFIG_TEMPLATE_FILE, 'w') as f:
        yaml.dump(CONFIG_TEMPLATE, f)
    print(f"Template config file {CONFIG_TEMPLATE_FILE} has been generated.")

def config_file_exists():
    return os.path.exists(CONFIG_FILE)

def load_config():
    if not config_file_exists():
        create_template_config()
        print(f"Template config file {CONFIG_TEMPLATE_FILE} has been generated.")
        exit(0)

    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def get_media_directory():
    return load_config()['media']['directory']


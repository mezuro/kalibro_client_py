import requests


DEFAULT_CONFIG = {'processor_address': "http://localhost:8082",
                  'configurations_address': "http://localhost:8083"}

_config = DEFAULT_CONFIG.copy()


# TODO: raise error if a not supported options is given
# TODO: read from YAML
def configure(processor_address=None, configurations_address=None, **opts):
    if processor_address:
        _config['processor_address'] = processor_address

    if configurations_address:
        _config['configurations_address'] = configurations_address


def config():
    return _config.copy()


def _clean_database(base_url):
    response = requests.post(base_url + '/tests/clean_database')
    response.raise_for_status()


def clean_processor():
    _clean_database(_config['processor_address'])


def clean_configurations():
    _clean_database(_config['configurations_address'])

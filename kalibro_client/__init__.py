# This tells Python that just configure and config should be visible
__all__ = ('configure', 'config')

DEFAULT_CONFIG = {'processor_address': "http://localhost:8082",
                  'configurations_address': "http://localhost:8083"}

_config = DEFAULT_CONFIG.copy()

# TODO: raise error if a not supported options is given
def configure(processor_address=None, configurations_address=None, **opts):
    if processor_address:
        _config['processor_address'] = processor_address

    if configurations_address:
        _config['configurations_address'] = configurations_address

def config():
    return _config.copy()

# TODO: read from YAML

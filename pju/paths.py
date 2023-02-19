import os

def data_dir():
    """Return the path to the data directory"""
    return os.path.join(os.path.expanduser('~'), '.pju')
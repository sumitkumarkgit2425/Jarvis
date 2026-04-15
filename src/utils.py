import os

def get_data_dir():
    """Returns the centralized path for JARVIS data, creating it if it doesn't exist."""
    data_dir = os.path.join(os.path.expanduser("~"), ".jarvis")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def get_file_path(filename):
    """Returns the absolute path for a data file in the centralized JARVIS directory."""
    return os.path.join(get_data_dir(), filename)

# ai/utils/data_handler.py

import pandas as pd

def load_data(filepath):
    """Loads encryption performance data from a CSV file."""
    return pd.read_csv(filepath)

def save_data(data, filepath):
    """Saves data to a CSV file."""
    data.to_csv(filepath, index=False)

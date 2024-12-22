import os 
import pandas as pd
import json
from IPython.display import display

def get_file_organization(verbose = False):
    """reads the filedata.json file where data file structure is organized."""
    base = os.getcwd()
    with open('filedata.json', 'r') as file:
        config = json.load(file)
    config['files'] = {key: os.path.join(base, value) for key, value in config.get('files', {}).items()}
    if verbose: 
        df = pd.DataFrame([
            {"Key": key, "File Path": value, "Explanation": config['explanation'][key]}
            for key, value in config['files'].items()
        ])
    # Use pandas display options for better formatting
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.expand_frame_repr', False)  # Don't wrap rows
    pd.set_option('display.max_rows', None)  # Show all rows
    
    display(df)
    return config['files']
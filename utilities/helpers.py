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


def extractor(full_title):
    """
        splits the job title into level and field values. 
        also contains some built in patches for typos and inconsistent synonyms.

        input: string
        output list of two strings : field/domain and title. 
    """
    full_title = full_title.strip().strip("'").strip()
    #delete stopwords; 
    full_title = full_title.replace(' of ', ' ').replace(' & ', ' ')
    field = ''
    title = ''
    if 'AI ' in full_title or 'Artificial Intelligence' in full_title:
        field = 'Artificial Intelligence'
    elif 'BI ' in full_title or 'Business Intelligence' in full_title:
        field = 'Business Intelligence'
    elif 'Big Data' in full_title:
        field = 'Big Data'
    elif 'Data Infrastructure' in full_title:
        field = 'Data Infrastructure'
    elif 'Data Analytics' in full_title:
        field = 'Data Analytics'
    elif 'Data Integration' in full_title:
        field = 'Data Integration'
    elif 'Robotics' in full_title:
        field = 'Robotics'
    elif 'Machine Learning' in full_title:
        field = 'Machine Learning'
    elif 'Data Quality' in full_title:
        field = 'Data Quality'
    elif 'Azure' in full_title or 'Cloud' in full_title:    #Azure is cloud computing
        field = 'Cloud'
    elif 'Computer Vision' in full_title:
        field = 'Computer Vision'
    elif 'Financial' in full_title or 'Finance' in full_title:
        field = 'Finance'
    elif full_title == 'Data Scientist':
        field = 'Data Science'

    
    #We'll not consider developer and programmer to be perfect synonyms. 
    #PATCH: Modeler and modeller are the same !!
    #PATCH: Data Analyst Lead and Data Analytics Lead are the same!!

    titles = ['Product Manager', 'Research Scientist', 'Data Analyst', 'Data Scientist', 'Product Owner',
              'Head of', 'Applied Scientist', 'Manager',  'Engineer', 'Director', 'Analyst', 'Modeler',
              'Architect', 'Developer', 'Programmer', 'Lead', 
              'Specialist', 'Technician', 'Consultant', 'Biologist', 'Associate', 
              'Scientist', 'Practitioner', 'Strategist', 'Researcher']
    for t in titles:
        if t in full_title:
            title = t
            break
    
    if field == '': 
        field = full_title.replace(title, '')

    field = field.strip()


    return [field, title]
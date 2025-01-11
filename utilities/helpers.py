import os 
import pandas as pd
import json
from IPython.display import display
import matplotlib.pyplot as plt
from rapidfuzz import process, fuzz

#standard style for plots: (helpers is imported in the notebook, so applied there. )
import matplotlib as mpl
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['figure.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.grid'] = False
mpl.rcParams['figure.figsize'] = [16, 9]
mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14

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

def is_employee_of_country(df):
    """adds a bool to df to indicate whether or not an entry is for an employee
      who has his residence in the same country as the company location."""
    df_internal = df.copy()
    df_internal['employee_of_country']  = df_internal['employee_residence'] == df_internal['company_location']
    return df_internal


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


def assign_country_codes(df_processed, income_df, processed_country_col, income_country_col, income_code_col, new_col_name):
    """
    Assigns the country codes from income_df to df_processed based on the highest fuzzy match score.
    
    Parameters:
        df_processed (pd.DataFrame): The dataframe to assign country codes.
        income_df (pd.DataFrame): The dataframe containing reference countries and their codes.
        processed_country_col (str): The column name in df_processed containing country names.
        income_country_col (str): The column name in income_df containing reference country names.
        income_code_col (str): The column name in income_df containing country codes.
    
    Returns:
        pd.DataFrame: The updated df_processed with an additional countrycode column.

    DISCLOSURE: Based on MWE made by ChatGPT, modified to fit needs.
    """
    # Create a mapping for country names to country codes
    country_to_code = dict(zip(income_df[income_country_col], income_df[income_code_col]))
    
    # Create a list of reference country names
    reference_countries = list(country_to_code.keys())
    
    # Initialize a column for country codes in df_processed
    df_processed[new_col_name] = None
    
    # Iterate through the rows in df_processed
    for index, row in df_processed.iterrows():
        # Get the country name from df_processed
        country_name = row[processed_country_col]
        
        # Find the best match for the country name in the reference list
        best_match, score, _ = process.extractOne(
            country_name, reference_countries, scorer=fuzz.token_sort_ratio
        )
        
        # Assign the corresponding country code if the match is confident enough
        if score > 80:  # Threshold for matching (adjust as needed)
            df_processed.at[index, new_col_name] = country_to_code[best_match]

    #patch for None values revealed by inspecting the unique_countries df: 
    #jersey is a british crown dependency, so we'll just assign it the code of the UK and be done with it.
    replacements = {
        'egypt': 'EGY', 
        'korea_': 'KOR', 
        'czechia': 'CZE', 
        'bahamas': 'BHS', 
        'hong_kong': 'HKG', 
        'jersey': 'GBR',
        'bolivia_plurinational_state_of': 'BOL'
        }
    for k,v in replacements.items():
        df_processed.loc[df_processed[processed_country_col] == k, new_col_name] = v

    
    return df_processed

def get_alphabetically(df, column):
    """Takes a pandas DF (df) and a string (column) which is the name of a column in df
    and returns an alphabetical list of values in that column. """
    l = df[column].unique()
    l.sort()
    return l 

def cleanup_strings(df, column, kvdict): 
    """Takes a pandas DF (df), a string (column) which is the name of a column in df 
    and a python dictionary in key(str)-value(str) formwat where key is the value 
    to be replace and value is the stringvalue it should be replaced with"""
    df = df.copy()
    df[column] = df[column].str.lower() #better for fuzzy matching required in stage 5
    for key, value in kvdict.items():
        df[column] = df[column].str.replace(key, value, regex=True)
    return df

def make_clusters(df, all_keys, exception_key): 
    """
        makes a groupby cluser of df based on all_keys with the exception of exception_key. 

        parametes:
            df = pandas dataframe (df_processed)
            all_keys = list of keys to group by
            exception_key = key to exclude from the groupby
    """
    groupkeys = all_keys.copy()
    groupkeys.remove(exception_key)
    cluster = (df.groupby(groupkeys)  # Group by these columns
        .size()
        .reset_index(name='count')  # Add counts as a new column
        .sort_values(by='count', ascending=False)  # Sort by counts in descending order
    )
    return cluster

def query_main_dataframe(row_index, combination_counts, main_df):
    """
    Query the main DataFrame for rows that match the constraints of a specified row in combination_counts.
    
    Parameters:
        row_index (int): The row index in combination_counts to use for constraints.
        combination_counts (pd.DataFrame): The DataFrame containing unique combinations and their counts.
            work_year, company_location, title, field, employment_type, work_setting, experience_level are required columns!!
            thus, these should be in your group by statement you use to generate the combination_counts Dataframe.
        main_df (pd.DataFrame): The main DataFrame to query.
        
    Returns:
        pd.DataFrame: A DataFrame with rows matching the constraints.
        string describing the constraints used for the query.
    """
    constraints = combination_counts.iloc[row_index]
    constraint_string = ''
    conditions = []
    for k,v in constraints.items():
        if k == 'count':   #I don't need count as a constraint: so skip it
            continue
        constraint_string += f"{k} == '{v}', "
        conditions.append(main_df[k] == v)
    #Build a query string: 
    final_condition = conditions[0]
    for condition in conditions[1:]:
        final_condition &= condition
    query_result = main_df[final_condition]  ##apply the queyr string
    return [query_result, constraint_string]  #return with explanation of what you queried

def make_company_var_plot(df, title, key): 
    """
        Plots from the main DataFrame a boxplot for wage vs xlabel variable.
    
    Parameters:
        df (pd.DataFrame): The main DataFrame to query.
        tutke (string): The title of the plot.
        xlabel (string): The column name to use for the x-axis and to determin behaviour of the funtciton. 
        
    Returns:
        plt boxplot with title.    
    """
    xlabel = ' '.join(key.split('_')).capitalize()
    # Predefined order of company sizes according to the given key
    if key  == 'company_size':
        order = ['S', 'M', 'L']  # Ensure order is maintained
    elif key == 'experience_level':
        order = ['Entry-level', 'Mid-level', 'Senior', 'Executive']
    elif key == 'work_setting': 
        order = ['In-person', 'Hybrid', 'Remote']
    elif key == 'employment_type': 
        order = ['Full-time' , 'Part-time', 'Freelance', 'Contract']
    
    # Prepare data for boxplots and count records for labels
    subset_data = []
    labels = []
    for size in order:
        size_data = df[df[key] == size]['target']
        subset_data.append(size_data)
        record_count = len(size_data)
        labels.append(f"{size} ({record_count})")  # Add count to label

    plt.boxplot(subset_data, tick_labels=labels)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Wage")
    return plt



def to_dataframe(X_transformed, transformer, columns):
    """converts a sparse dataframe back to a normal pndas dataframe"""
    if hasattr(X_transformed, "toarray"):  # Check if the result is a sparse matrix
        X_transformed = X_transformed.toarray()  # Convert to dense
    # If the transformer has feature names, use them; otherwise, use a range of integers
    if hasattr(transformer, 'get_feature_names_out'):
        new_columns = transformer.get_feature_names_out(columns)
    else:
        new_columns = range(X_transformed.shape[1])  # Fallback for when feature names are not available
    return pd.DataFrame(X_transformed, columns=new_columns)


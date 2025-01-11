# Regression task - assignment 2: 
https://github.com/Frederic-P/evaluatie-2---regressie 

## PIP installatie
VENV is managed by PIP not Anaconda. tested on python 3.11.0

open PowerShell in the directory where you want to create a venv for this project. If needed use `cd` to navigate to the required direcotry. It is okay to just download this repo, unzip it and create the venv in here.
type: `python -m venv .` **the final dot is important**, it will create the venv in the directory your powerShell is in. Run this command with your Python 3.11.0 installation!! - if you have multiple Python installations, make sure to use the correct one; it could be that the venv install command becomes `python3.11 -m venv .` depending on your system and Path. After making the virtual environment, run the following steps: 
- activate the venv: `scripts/activate`
- install requirements: `pip install -r requirements.txt`
- wait for pip installation to complete.
- launch notebook: `jupyter notebook` or open in VSCODE and use the installed kernel to run the notebook there. 
- Run all cells. 

## Data directory/management.
- Excel used for training the data should be in the `data/raw` directory and should be called `jobs_dataset_without_solution.xls`
- CSV file used for testing the data should be in the `data/raw` directory and should be called `y_test.csv`

## Data engineering
- Data is downloaded from the World Bank to generate Income classes and GDP/capita; an active internet connection is required and write permission to the `data/raw` directory is needed. Code for caching downloaded files and checking for existence is not implemented, so the notebook will download the file each time (pros and cons to this approach). 

## Notebook organization
All code is organized into a single notebook and can just be ran from top to bottom. The notebook is called `notebook.ipynb` and is located in the root of the project. The notebook is divided into four sections with clear headings. Structure of the notebook is like this: 

```
SECTION A: sectiontitle. (H1 ALLCAPS)
    1) MainTitle (H1 Normal case)
        1.1) Subtitle (H2 Normal case)
        1.2) Subtitle
        ...
    2) MainTitle
SECTION B: 
....

```

## Output
- The notebook will output a CSV file called `y_test.csv.csv` in the `data/output` folder - write permission on the `data` folder is required.

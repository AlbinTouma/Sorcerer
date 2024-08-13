import pandas as pd
import re
import ast
from ast import literal_eval
import pyarrow as pa
import pyarrow.parquet as pq
import json
import numpy as np

"""This script extracts the occupation of a PEP and checks if that PEP has a valid occupation. If occupation is invalid the PEP is marked as such"""

def load_keywords():
    keywords = pd.read_csv('templates/PEP_keywords.csv')
    # Create a list
    keywords = keywords['occupation'].to_list()
    # Lowercase
    keywords = [keyword.lower() for keyword in keywords]
    return keywords


# Convert ids to RCA/PEP
def pep_id(df):
    df['PEP_id'] = [False if re.search(
        '_\d+$', id) else True for id in df['_id']]
    return df

# Load keyword template


def remove_keyword_in_parenthesis(text):
    while '(' in text and ')' in text:
        start = text.find('(')
        end = text.find(')')
        if start < end:
            text = text[:start] + text[end + 1:]
        else:
            break
    return text


def validate_occupation(occupation_array, keywords):
    matching_keywords = []

    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        exclude_phrase = ['Child of ', 'Spouse of ']

        # If row is an array, for each item in array, remove () and match item of array to pattern. If item fits pattern and does not have Child of/Parent of, append to our list.
        if isinstance(occupation_array, np.ndarray):
            for item in occupation_array:
                clean_occupation_str = remove_keyword_in_parenthesis(item)
                if re.search(pattern, clean_occupation_str, re.IGNORECASE) and not any(phrase in clean_occupation_str for phrase in exclude_phrase):
                    matching_keywords.append(keyword)

        # For values that are NAN and not in an array
        else:
            return False, []

    # Return True if there's values in array, and the keyword
    return bool(matching_keywords), matching_keywords


def main(file_path, parquet_file):
    keywords = load_keywords()
    df = pd.read_parquet(f'{file_path}')

    if not df.empty:
        if "DBPedia" in file_path:
            df = pep_id(df)

    try:
        if '_source.data.occupations.occupation' in df.columns:
            df['has_occupation'] = df['_source.data.occupations.occupation'].apply(
                lambda x: validate_occupation(x, keywords)[0])
            df['occupation_keywords'] = df['_source.data.occupations.occupation'].apply(
                lambda x: validate_occupation(x, keywords)[1])
        elif '_source.data.occupations.occupation' not in df.columns:
            df['has_occupation'] = df['_source.data.display_fields.value'].apply(
                lambda x: validate_occupation(x, keywords)[0])
            df['occupation_keywords'] = df['_source.data.display_fields.value'].apply(
                lambda x: validate_occupation(x, keywords)[1])

    except Exception as e:

        df['has_occupation'] = False
        df['occupation_keywords'] = None

    df.to_parquet(f'parquet/{parquet_file}')


if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
from datetime import datetime, date
import math
import json

# Convert string date to timestamp
def convert_str_to_date(row):
    '''Convert array of string dates to timestamp dates'''
    date_format = '%Y-%m-%d'
    if row is None:
        return None
    else:
        for date_str in row:
            if date_str is None:
                pass
            else:
                date_obj = datetime.strptime(date_str, date_format)
                return date_obj


# Calculate the age from birth
def calculate_age(row):
    today = date.today()
    age = today.year - row.year - \
        ((today.month, today.day) < (row.month, row.day))
    return age


# Score where age follows rule
def score(age):
    if pd.isnull(age) or age < 18 or age > 200:
        return 0
    else:
        return 1


def return_score(min_age, max_age):
    return max(min_age, max_age)


def score_age(min_age, max_age):
    min_age = min_age.apply(lambda x: score(x))
    max_age = max_age.apply(lambda x: score(x))
    result = pd.concat([min_age, max_age], axis=1)
    age_score = result.apply(lambda row: return_score(row[0], row[1]), axis=1)
    return age_score


def work_out_age(df):
    dob_fields = ['_source.data.births.has_dob', '_source.data.births.has_enrichment_dob_source',
                  '_source.data.births.min_date', '_source.data.births.max_date']

    if any(col in df.columns for col in dob_fields):
        df['_source.data.births.min_date'] = df['_source.data.births.min_date'].apply(
            lambda x:  convert_str_to_date(x))
        df['_source.data.births.max_date'] = df['_source.data.births.max_date'].apply(
            lambda x:  convert_str_to_date(x))
        df['min_age'] = df['_source.data.births.min_date'].apply(
            lambda x: calculate_age(x))
        df['max_age'] = df['_source.data.births.max_date'].apply(
            lambda x: calculate_age(x))
        df['score.age'] = score_age(df['min_age'], df['max_age'])
    else:
        df['score.age'] = 0
    return df

# Location and general come as array. We convert the arrays to lists
def convert_array_to_list(array):
    if array is not None:
        return [item if item is not None else None for item in array]
    return None


def lists_to_dict(location_type, location_name):
    result_list = []
    for type, name in zip(location_type, location_name):
        if type is not None and name is not None:
            result = {}
            for key, value in zip(type, name):
                if key is not None:
                    result[key] = value if value is not None else None
            result_list.append(result)
        else:
            # Append None if either type or name is None
            result_list.append(None)
    return result_list
# In this updated code, we append None to the result_list when either location_type or location_name is None, and an empty dictionary is added to the list for pairs where both location_type and location_name are not None. This ensures that the result list contains either dictionaries or None values based on the presence of None in the input series.


def create_dictionary(location_type, location_name):
    location_type = pd.Series([convert_array_to_list(array)
                              for array in location_type])
    location_name = pd.Series([convert_array_to_list(array)
                              for array in location_name])
    dictionary_result = pd.Series(lists_to_dict(location_type, location_name))

    return dictionary_result


def extract_scores_from_location_dictionary(row):
    place_of_birth = 0
    general = 0

    if row is not None:
        if 'place_of_birth' in row and row['place_of_birth'] is not None:
            place_of_birth = 1

        if 'general' in row and row['general'] is not None:
            general = 1

    return place_of_birth, general


def score_location(df):
    '''Score whether there is key: general|place_of_birth and if it has a value'''

    location_fields = ['_source.data.locations.name',
                       '_source.data.locations.location_type']

    # If all asset columns are present then execute score_picture fields. If not then award 0 as both are required.
    if all(col in df.columns for col in location_fields):

        df['dictionary_result'] = create_dictionary(
            df['_source.data.locations.location_type'], df['_source.data.locations.name'])
        df['score.place_of_birth'] = df['dictionary_result'].apply(
            lambda x: extract_scores_from_location_dictionary(x)).apply(lambda x: x[0])
        df['score.location'] = df['dictionary_result'].apply(
            lambda x: extract_scores_from_location_dictionary(x)).apply(lambda x: x[1])
    else:
        df['score.place_of_birth'] = 0
        df['score.location'] = 0

    return df


def check_for_image_type(lst):
    if lst is not None:
        return 'image' in lst
    if lst is None:
        return False


def check_for_external_urls(lst):
    if lst is not None:
        for item in lst:
            if item:
                return True
    if lst is None:
        return False


def score_picture(asset_types, external_urls):

    # Convert asset_types and external urls to list
    asset_types = pd.Series([convert_array_to_list(array)
                            for array in asset_types])
    external_urls = pd.Series([convert_array_to_list(array)
                              for array in external_urls])

    # Check if there is image in list of assets.types
    is_image = asset_types.apply(check_for_image_type)

    # Check if there's a value for URL
    is_url = asset_types.apply(check_for_external_urls)

    # Score 1 if image and url are both true
    picture_score = (is_image & is_url).astype(int)

    return is_image, is_url, picture_score


def execute_score_picture(df):
    asset_fields = ['_source.assets.asset_types',
                    '_source.assets.external_urls']

    # If all asset columns are present then execute score_picture fields. If not then award 0 as both are required.
    if all(col in df.columns for col in asset_fields):
        df['is_image'], df['is_url'], df['score.picture'] = score_picture(
            df['_source.assets.asset_types'], df['_source.assets.external_urls'])
    else:
        df['score.picture'] = 0

    return df


def score_occupation(array):
    return array.astype(int)


def execute_score_occupation(df):
    df['score.occupation'] = score_occupation(df['has_occupation'])
    return df


def extract_related_url(series_dictionary):
    exclude_urls = ['http://complyadvantage.com',
                    'https://complyadvantage.com']
    url_correct = 0
    # for row in series_dictionary:
    if series_dictionary is not None:
        related_url_value = series_dictionary.get('Related Url')

        if related_url_value:
            if not any(exclude_url in related_url_value for exclude_url in exclude_urls):
                url_correct = 1
                # print(f'related_url value is {related_url_value}')
            else:
                url_correct = 0
                # print(f'contains {substring_to_exclude}')
        else:
            url_correct = 0
            # print('The related url is not in dictionary')
    return url_correct

    # Need to extract them as dictionary


# df[['_source.data.display_fields.title', '_source.data.display_fields.value']].value_counts()
def related_urls(display_fields_title, display_fields_value):
    # Convert array list
    display_fields_title = pd.Series(
        [convert_array_to_list(array) for array in display_fields_title])
    display_fields_value = pd.Series(
        [convert_array_to_list(array) for array in display_fields_value])

    # Convert lists into dictionary
    dictionary_result = pd.Series(lists_to_dict(
        display_fields_title, display_fields_value))
    url_correct = dictionary_result.apply(lambda x: extract_related_url(x))

    return url_correct


def execute_score_related_urls(df):
    url_fields = ['_source.data.display_fields.title',
                  '_source.data.display_fields.value']
    if all(col in df.columns for col in url_fields):
        df['score.related_url'] = related_urls(
            df['_source.data.display_fields.title'], df['_source.data.display_fields.value'])
    else:
        df['score.related_url'] = 0

    return df


# Check if the list in our political columns has a value
def has_non_none_value(lst):
    if lst is not None:
        return 1 if any(item is not None for item in lst) else 0
    return 0


# Loop through our scored columns. If there's 1 then add1 for political score
def has_political_fields(row, columns):
    for col in columns:
        if row[f'score.{col}'] == 1:
            return 1
    return 0


def execute_political_fields(df):
    # Political columns that we're interested in
    political_columns = ['_source.data.aml_types.end_date',
                         '_source.data.aml_types.start_date', '_source.data.display_fields.value']

    # For each column in our political columns, convert array to list; check if there's a value and score 1, then for our columns, check if any of them has 1 and return 1 for politics.
    for col in political_columns:
        try:
            col_series = pd.Series([convert_array_to_list(array)
                                    for array in df[col]])
            df[f'score.{col}'] = df[col].apply(has_non_none_value)
        except KeyError:
            df[f'score.{col}'] = 0

    df['score.political_fields'] = df.apply(
        has_political_fields, columns=political_columns, axis=1)

    return df


def execute_score_gender(df):
    gender_field = ['_source.data.genders.gender']
    if '_source.data.genders.gender' in df.columns:
        gender = pd.Series([convert_array_to_list(array)
                           for array in df['_source.data.genders.gender']])
        df['score.gender'] = gender.apply(has_non_none_value)
    else:
        df['score.gender'] = 0

    return df


category_weight = {
    "primary": 0.5,
    "secondary": 0.35,
    "other": 0.15
}


# This applies multipliers to each score
def apply_scoring_system(df):
    # Load the multipliers for each score  in scoring_system.json
    with open('templates/scoring_system.json', 'r') as file:
        scoring_system = json.load(file)

    # Iterate through columns in df. If column is in scoring_json then apply multiplier.
    for column in df.columns:
        if column in scoring_system:
            df[column] *= scoring_system[column]

    return df


# Sums weighted scores by primary, secondary and other.
# DQS is the sum of primary, secondary, other.
def data_quality_score(df):
    primary_identifiers = ['score.age',
                           'score.place_of_birth', 'score.picture']
    secondary_identifiers = [
        'score.location', 'score.occupation', 'score.picture', 'score.political_fields']
    other_identifiers = ['score.related_url', 'score.gender']

    df['score.primary'] = df[primary_identifiers].sum(axis=1)
    df['score.secondary'] = df[secondary_identifiers].sum(axis=1)
    df['score.other'] = df[other_identifiers].sum(axis=1)

    df['score.data_quality'] = df[['score.primary',
                                   'score.secondary', 'score.other']].sum(axis=1)

    return df


def main(file_path, parquet_file):

    df = pd.read_parquet(f'{file_path}')
    if not df.empty:

        df = work_out_age(df)
        df = score_location(df)
        df = execute_score_picture(df)
        df = execute_score_occupation(df)
        df = execute_score_related_urls(df)
        df = execute_political_fields(df)
        df = execute_score_gender(df)
        df = apply_scoring_system(df)
        df = data_quality_score(df)
        df.sort_values(by='score.data_quality', ascending=False)

        df.to_parquet(f'parquet/{parquet_file}')


if __name__ == "__main__":
    main()

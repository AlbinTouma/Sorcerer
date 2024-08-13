import os
import pandas as pd
from fetchdata_module import make_api_call, clean_data
from dataquality_module import extract_peps, complete_profiles, profile_quality
from dataquality_module import assess_names, delete_logic
from tqdm import tqdm


def load_data():
    input_directory = 'input'
    input_files = [f for f in os.listdir(
        input_directory) if f.endswith('.xlsx')]

    source_id = []
    source_name = []

    for input_file in input_files:
        input_file_path = os.path.join(input_directory, input_file)
        data = pd.read_excel(input_file_path, sheet_name='Sheet1')

        source_id.extend(data['source_id'])
        source_name.extend(data['name'])

    return source_id, source_name


def fetch_data():
    source_id, source_name = load_data()

    for i in tqdm(range(len(source_id))):
        source_id_value = source_id[i]
        source_name_value = source_name[i]

        make_api_call.main(source_name_value, source_id_value)


class ParquetUtility:
    def __init__(self, parquet_directory):
        self.parquet_directory = parquet_directory

    def list_parquet_files(self):
        parquet_files = [f for f in os.listdir(
            self.parquet_directory) if f.endswith('.parquet')]
        return parquet_files

    def construct_file_path(self, parquet_file):
        return os.path.join(self.parquet_directory, parquet_file)


def process_data():
    parquet_utility = ParquetUtility('parquet')
    parquet_files = parquet_utility.list_parquet_files()

    for parquet_file in tqdm(parquet_files):
        input_file_path = parquet_utility.construct_file_path(parquet_file)

        clean_data.main(input_file_path, parquet_file)


def extract_PEP_occupation():
    parquet_utility = ParquetUtility('parquet')
    parquet_files = parquet_utility.list_parquet_files()

    for parquet_file in tqdm(parquet_files):
        input_file_path = parquet_utility.construct_file_path(parquet_file)

        extract_peps.main(input_file_path, parquet_file)


def completeness():
    parquet_utility = ParquetUtility('parquet')
    parquet_files = parquet_utility.list_parquet_files()

    for parquet_file in tqdm(parquet_files):
        input_file_path = parquet_utility.construct_file_path(parquet_file)
        complete_profiles.main(input_file_path, parquet_file)


def quality():
    parquet_utility = ParquetUtility('parquet')
    parquet_files = parquet_utility.list_parquet_files()

    for parquet_file in tqdm(parquet_files):
        input_file_path = parquet_utility.construct_file_path(parquet_file)
        profile_quality.main(input_file_path, parquet_file)


def asses_completeness_names():
    parquet_utility = ParquetUtility('parquet')
    parquet_files = parquet_utility.list_parquet_files()

    for parquet_file in tqdm(parquet_files):
        input_file_path = parquet_utility.construct_file_path(parquet_file)
        assess_names.main(input_file_path, parquet_file)


def profiles_to_delete():
    parquet_utility = ParquetUtility('parquet')
    parquet_files = parquet_utility.list_parquet_files()

    for parquet_file in tqdm(parquet_files):
        input_file_path = parquet_utility.construct_file_path(parquet_file)
        delete_logic.main(input_file_path, parquet_file)


def main():
    load_data()
    print('Fetching data')
    fetch_data()
    process_data()
    print('Completed fetching data')
    print('Extracting PEPs occupation')
    extract_PEP_occupation()
    print('Completed Extracting PEP occupations')
    print('Running completeness')
    completeness()  # Complete
    print('Completed Completeness Checks')
    print("Running quality logic")
    quality()
    print('Completed quality checks')
    print("Flagging names")
    asses_completeness_names()
    print("Flagging profiles to delete")
    profiles_to_delete()
    print('Completion')


main()

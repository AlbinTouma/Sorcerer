import pandas as pd
import numpy as np

'''This script checks for structural problems in our data by screening completeness ie whether a dataframe has a data field. '''

def generate_identifiers():
    def generate_primary_identifiers():
        return {
            'Name': ['_source.data.names.aliases', '_source.data.display_fields.title'],
            'DoB': ['_source.data.births.age', '_source.data.births.max_date', '_source.data.births.min_date'],
            'Location': ['_source.data.locations.location_type'],
            'Assets': ['_source.assets.photo_count', '_source.assets.assets_types', '_source.assets.assets.external_urls']
        }

    def generate_secondary_identifiers():
        return {
            'Gender': ['_source.data.genders.gender'],
            'Location': ['_source.data.locations.name', '_source.data.locations.locations_count'],
            'Political Scope': ['_source.data.aml_types.aml_type', '_source.data.aml_types.end_date', '_source.data.aml_types.start_date', '_source.data.occupations.occupation']
        }

    primary_identifiers = generate_primary_identifiers()
    secondary_identifiers = generate_secondary_identifiers()

    return primary_identifiers, secondary_identifiers


def identify_non_null(value):
    # If value is a list or array, iterate to see if there's notna value. Else, check if value is notna.
    return int(any(pd.notna(val) for val in value)) if isinstance(value, (list, np.ndarray)) else int(pd.notna(value))


def identify_notna(value):
    # If value is a list or array, iterate to see if there's notna value. Else, check if value is notna.
    return any(pd.notna(val) for val in value) if isinstance(value, (list, np.ndarray)) else pd.notna(value)


def count_data_in_columns(row, selected_columns):
    count = sum(1 if identify_notna(
        row[column]) else 0 for column in selected_columns)
    name = True if any(pd.notna(val)
                       for val in row['_source.data.names.name']) else False
    # Might need to add condition that checks if there's a value for at least one in political scope (True/False)

    return count, name


def completeness_classifier(row):
    primary_value, secondary_value = row['Primary'], row['Secondary']

    status = 'complete' if primary_value[0] >= 1 and secondary_value[0] >= 2 else \
        'sufficient' if primary_value[0] >= 1 and secondary_value[0] < 1 or primary_value[0] < 1 and secondary_value[0] > 2 else \
        'insufficient' if primary_value[0] < 1 else None

    return status


def main(file_path, parquet_file):
    df = pd.read_parquet(f'{file_path}')
    if not df.empty:

        # Generate primary_identifiers and extract identifier columns as primary and secondary lists
        primary_identifiers, secondary_identifiers = generate_identifiers()
        primary_identifiers = [
            item for value_list in primary_identifiers.values() for item in value_list]
        secondary_identifiers = [
            item for value_list in secondary_identifiers.values() for item in value_list]

        # Dynamically choose the primary and secondary columns that are in our dataframe
        primary_data_columns = df.columns[df.columns.isin(
            primary_identifiers)].to_list()
        secondary_data_columns = df.columns[df.columns.isin(
            secondary_identifiers)].to_list()

        # Count non_nans and if df has a name by passing primary and secondary columns to count_data_in_columns function
        df['Primary'] = df.apply(count_data_in_columns,
                                 selected_columns=primary_data_columns, axis=1)
        df['Secondary'] = df.apply(
            count_data_in_columns, selected_columns=secondary_data_columns, axis=1)
        df['Primary'] = [list(item) for item in df['Primary']]
        df['Secondary'] = [list(item) for item in df['Secondary']]

        # Apply the completness criteria to each row in the dataframe to identify profiles that are complete, sufficient, or insufficient
        df['completeness'] = df.apply(completeness_classifier, axis=1)

        df['Primary'] = df['Primary'].apply(str)
        df['Secondary'] = df['Secondary'].apply(str)

        df.to_parquet(f'parquet/{parquet_file}')


if __name__ == "__main__":
    main()

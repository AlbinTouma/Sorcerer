import pandas as pd
import numpy as np
from ast import literal_eval


def select_columns(df) -> any:
    '''Selects fields from _id, _source.data, _source.assets, and _source.source_data'''
    pattern = r'^(_id|_source\.(data|assets|source_data|sources.source_ids))'
    filtered_columns = df.columns.str.contains(pattern, regex=True)
    df = df.loc[:, filtered_columns]
    return df


def remove_parent_keys(column):
    '''Df contains parent keys. We remove all of them by removing any column wit {}. We also remove _source.source_data which starts with [{'''
    return any(isinstance(value, str) and (value.startswith('{') or value.startswith('[{')) for value in column)


def row_to_nan(row):
    '''Convert [NaN, NaN] values in list to NaN'''
    try:
        row_list = eval(row)
        if all(val is None for val in row_list):
            return np.nan
    except (ValueError, SyntaxError, NameError, TypeError):
        pass
    return row


def main(file_path, parquet_file):
    df = pd.read_parquet(f'{file_path}')

    if not df.empty:

        df = select_columns(df)

        remove_columns = [
            column for column in df if remove_parent_keys(df[column])]
        df = df.drop(columns=remove_columns)

        for column in df.columns:
            df[column] = df[column].apply(row_to_nan)

        df.to_parquet(f'parquet/{parquet_file}')



if __name__ == '__main__':
    main()

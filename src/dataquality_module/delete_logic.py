import pandas as pd


def count_profiles_to_delete(df):
    combined_condition = (df['score.data_quality'] < 0.5) | (df['TOTAL_FLAGS'] > 0)| (df['score.age'] == 0) | (df['has_occupation'] == False)
    df['score.delete_profile'] = combined_condition
    return df


def main(input_file_path, parquet_file):
    df = pd.read_parquet(f'{input_file_path}')
    df = df.apply(count_profiles_to_delete, axis=1)
    df.to_parquet(f'parquet/{parquet_file}')


if __name__ == "__main__":
    main()

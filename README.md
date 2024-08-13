# 🧙 Sorcerer

Sorcerer is a programme written in Python that lets users query, download, and review PEP sources in bulk. Sorcerer was designed to help the PEP team analyse PEP data faster, and overcome Kibana’s 10MB download rate.

This project is split into Notebooks for testing and an src folder containing python modules.

```
.
├── notebook
│   └── Method
│       ├── 01_fetch_data
│       └── 02_data_quality
└── src
    ├── dataquality_module
    │   └── __pycache__
    ├── fetchdata_module
    │   └── __pycache__
    ├── input
    ├── parquet
    └── templates
		
```
## Run Sorcerer

You run Sorcerer by placing an Excel file with the sources you want to analyse. The file must contain the following fields: 

```
source_id, name
S:KH10AL, quicky_for_erika
```

You can now run Sorcerer. Sources will be fetched from Kibana using ElasticSearch and stored as parquet files in the parquet folder.

## Modules

### Fetch data module

The make_api_call.py iterates through the list of sources and gets using ElasticSearch query. Data is then saved to a parquet file that the clean_data.py uses.

`clean_data.py` prepares the PEP sources. The script:

1. Filters keys and selects data in `_id`, `_source.data`, `_source.assets` and `sources.source_ids`.
2. Removes parent keys
3. Converts [NaN, NaN] values in lists to just NaN
4. Saves files as parquet

### Data Quality Module

- `complete_profiles.py` checks for structural problems in our data by screening completeness ie whether a dataframe has a data field.
- `extract_peps.py` extracts the occupation of a PEP and checks if that PEP has a valid occupation. If occupation is invalid the PEP is marked as such
- `profile_quality.py` scores data fields based on our data quality schema and returns scores and a data quality score from 0-100 where 100 represents perfect quality.
- `assess_names.py` checks PEP's names and identifies invalid names. 
- `delete_logic.py` checks data quality score, name, and occupation and flags profiles that should be deleted

The files rely on templates. 
- `Scoring_system.json` contains the data quality schema that we use to convert scores on different fields
- `PEP_keywords.csv` contains PEP related occupation keywords for different langauges. We use this list when evaluating occupation of a PEP profile.
- `constants.py` contains lists of keywords and stopwords used in assessing PEP names. 









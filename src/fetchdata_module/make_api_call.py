import requests
import traceback
import json
import timeit
import pandas as pd


url = ELASTIC_SEARCH_URL 
scroll_time = "1m"
page_size = 10000

# Build the query based on the source_id.


def build_query(source_id):
    query_comp1 = {
        "size": page_size,
        "query": 
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "source_ids_original": f"{source_id}"
                        }
                    },
                    {
                        "match_phrase": {
                            "meta.document_type_code": "SM"
                        }
                    }
                ]
            }
        },
        "sort": [{"meta.updated_utc": {"order": "desc"}}]
    }

    query = {**query_comp1}

    return query

# Build the elastic search query and fetch the API with scroll


def elastic_search(source_id):
    # Container for all retrieved documents
    all_documents = []
    query = build_query(source_id)

    try:
        # Initial search request with scroll parameter in the query string
        r = requests.post(
            url + "?scroll=" + scroll_time, json=query)

        res = r.json()

        # Extract the initial results
        hits = res.get('hits').get('hits')
        all_documents.extend(hits)

        # Get the scroll ID for the next page
        scroll_id = res.get("_scroll_id")

        while True:
            # Perform the scroll using POST request
            scroll_response = requests.post(
                ELASTIC_ENDPOINT, json={"scroll": scroll_time, "scroll_id": scroll_id})
            scroll_data = scroll_response.json()

            if "hits" not in scroll_data or not scroll_data.get('hits', {}).get('hits', []):
                break  # No more results to retrieve

            # Append the new results to the existing hits
            hits = scroll_data["hits"]["hits"]
            all_documents.extend(hits)

            # Get the scroll ID for the next page
            scroll_id = scroll_data["_scroll_id"]

    except Exception as e:
        traceback.print_exc()
        print(f"Error while retrieving data: {str(e)}")

    # print(f"Total documents retrieved: {len(all_documents)}")

    return all_documents


def normalise_response(response):
    normalised_df = pd.json_normalize(response)
    return normalised_df


def main(source_name, source_id):
    response = elastic_search(source_id)
    normalised_response = normalise_response(response)
    normalised_response.to_parquet(
        f'parquet/{source_name}.parquet')


if __name__ == '__main__':
    main()

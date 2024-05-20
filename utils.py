import requests
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def get_metrics(url: str, headers: dict, params: dict) -> list:
    try:
        insights = []

        while True:
            r = requests.get(url=url, headers=headers, params=params)
            insight_data = r.json()

            if "error" in insight_data:
                print("Error:", insight_data["error"])
                break

            insights.extend(insight_data["data"])

            # Check for pagination
            if (
                "paging" in insight_data
                and "cursors" in insight_data["paging"]
                and "after" in insight_data["paging"]["cursors"]
            ):
                params["after"] = insight_data["paging"]["cursors"]["after"]
            else:
                break
        return insights
    except Exception as e:
        return str(r)

def get_big_query_information(table: str, dataset_id: str, project_id: str):
    try:
        table_id = "{}.{}.{}".format(project_id, dataset_id, table)
        return table_id
    except Exception as e:
        return str(e)


def load_table_dataframe(
    key_path: str, project_id: str, table_id: str, dataframe: pd.DataFrame
):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        # Construct a BigQuery client object.
        client = bigquery.Client(credentials=credentials, project=project_id)

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)
        job.result()

        data = client.get_table(table_id)
        return data
    except Exception as e:
        return str(e)

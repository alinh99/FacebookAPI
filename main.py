from flask import Flask
from google.cloud import bigquery
from utils import get_metrics
import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
API_VERSION = "v19.0"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
AD_ACCOUNT_ID = os.environ.get("AD_ACCOUNT_ID", "")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "facebook-ads-423612-19b305fc6869.json"
url = f"https://graph.facebook.com/{API_VERSION}/act_{AD_ACCOUNT_ID}/insights"

params = {
    "fields": "ad_name, adset_name, campaign_name, spend, impressions, reach, cost_per_conversion, frequency, inline_link_clicks, ctr, cpm, cpc, clicks, date_start, ad_id",
    "date_preset": "maximum",
    "time_increment": 1,
    "limit": 100,  # Adjust as needed
    "level": "ad",
}
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

dataset_id = os.environ.get("DATASET_ID", "")
project_id = os.environ.get("PROJECT_ID", "")
credential_file = "facebook-ads-423612-19b305fc6869.json"
table_name = os.environ.get("TABLE_NAME", "")


# Run flask app with one default URL and other with 'append_data' which will be scheduled
app = Flask(__name__)


@app.route("/")
def hello():
    return "App is running to load Facebook Ads data every 24 hours!"


@app.route("/append_facebook_data")
def append_data():
    """Return a friendly HTTP greeting."""
    data = get_metrics(url, headers, params)

    insight_data_df = pd.DataFrame(data)

    insight_data_df.drop(columns="date_stop", inplace=True)

    client = bigquery.Client()

    print("size of dataframe = " + str(insight_data_df.shape[0]))

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

    job = client.load_table_from_dataframe(
        insight_data_df, f"{project_id}.{dataset_id}.{table_name}",
        job_config=job_config
    )
    job.result()

    print(
        "Total Facebook Ads records logged to BigQuery =  "
        + str(insight_data_df.shape[0])
    )

    return "Results Logged for Facebook Ads!"

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=False)

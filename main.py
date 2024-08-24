from flask import Flask
from google.cloud import bigquery
from utils import get_metrics
import os
import pandas as pd
from dotenv import load_dotenv
import traceback
import sys
import logging

load_dotenv()

# Run flask app with one default URL and other with 'append_data' which will be scheduled
app = Flask(__name__)


@app.route("/")
def hello():
    return "App is running to load Facebook Ads data every 24 hours!"


@app.route("/append_facebook_data")
def append_facebook_data():
    """Return a friendly HTTP greeting."""
    try:
        ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
        AD_ACCOUNT_ID = os.environ.get("AD_ACCOUNT_ID", "")
        APP_ID = os.environ.get("APP_ID", "")
        APP_SECRET = os.environ.get("APP_SECRET", "")
        # ACCESS_TOKEN = exchange_token(SHORT_ACCESS_TOKEN, APP_ID, APP_SECRET)
        
        params = {
            "fields": "ad_name, adset_name, campaign_name, spend, impressions, reach, cost_per_conversion, frequency, inline_link_clicks, ctr, cpm, cpc, clicks, date_start, ad_id",
            "date_preset": "maximum",
            "time_increment": 1,
            "limit": 100,  # Adjust as needed
            "level": "ad",
        }

        dataset_id = os.environ.get("DATASET_ID", "")
        project_id = os.environ.get("PROJECT_ID", "")
        table_name = os.environ.get("TABLE_NAME", "")
        
        data = get_metrics(
            ad_account_id=AD_ACCOUNT_ID,
            params=params,
            APP_ID=APP_ID,
            APP_SECRET=APP_SECRET,
            ACCESS_TOKEN=ACCESS_TOKEN,
            limit=params["limit"]
        )

        insight_data_df = pd.DataFrame(data)

        if "date_stop" in insight_data_df.columns:
            insight_data_df.drop(columns="date_stop", inplace=True)

        client = bigquery.Client()

        print("size of dataframe = " + str(insight_data_df.shape[0]))

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        job = client.load_table_from_dataframe(
            insight_data_df,
            f"{project_id}.{dataset_id}.{table_name}",
            job_config=job_config,
        )
        job.result()

        return "Results Logged for Facebook Ads!"
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}, Exception type: {ex_type}, Exception message: {ex_value}"
            )
        stack_trace_message = "\n".join(stack_trace)
        logging.error(
            f"Exception type: {ex_type}, Exception message: {ex_value}\nStack trace:\n{stack_trace_message}"
        )
        print(f"Exception type: {ex_type}, Exception message: {ex_value}\nStack trace:\n{stack_trace_message}")
        return f"Exception type: {ex_type}, Exception message: {ex_value}\nStack trace:\n{stack_trace_message}"


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=False)

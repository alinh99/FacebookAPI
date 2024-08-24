import time
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
import traceback
import sys
import logging
import requests

def wait_for_async_job(job, limit: int, TIMEOUT=300):
    try:
        for _ in range(TIMEOUT):
            time.sleep(1)
            job = job.api_get()
            status = job[AdReportRun.Field.async_status]
            if status == "Job Completed":
                return job.get_result(params={"limit": limit})
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
        return  f"Exception type: {ex_type}, Exception message: {ex_value}\nStack trace:\n{stack_trace_message}"

def exchange_token(short_lived_token, client_id, client_secret):
    exchange_url = f"https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={client_id}&client_secret={client_secret}&fb_exchange_token={short_lived_token}"
    response = requests.get(exchange_url)
    long_lived_token = response.json().get('access_token')
    return long_lived_token

def get_metrics(ad_account_id: str, params: dict, APP_ID: str, APP_SECRET: str, ACCESS_TOKEN: str, limit: int, timeout=300)->list:
    try:
        FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
        job = AdAccount(f'act_{ad_account_id}').get_insights_async(params=params)
        result_cursor = wait_for_async_job(job, limit, timeout)
        results = [item for item in result_cursor]
        return results
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
        return  f"Exception type: {ex_type}, Exception message: {ex_value}\nStack trace:\n{stack_trace_message}"

from dotenv import load_dotenv
import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import pandas as pd
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adreportrun import AdReportRun
load_dotenv()

access_token =  os.environ.get('ACCESS_TOKEN', '')
app_id = os.environ.get('APP_ID', '')
app_secret = os.environ.get('APP_SECRET', '')
ad_account_id = os.environ.get('AD_ACCOUNT_ID', '')

# Initialize the Facebook Ads API
FacebookAdsApi.init(app_id, app_secret, access_token)

# Define the fields and parameters for the request
fields = [
    AdsInsights.Field.ad_id,
    AdsInsights.Field.ad_name,
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.adset_name,
    AdsInsights.Field.impressions,
    AdsInsights.Field.spend,
    AdsInsights.Field.campaign_id,
    AdsInsights.Field.date_start,
    AdsInsights.Field.date_stop,
    AdsInsights.Field.dda_results,
    AdsInsights.Field.cost_per_conversion,
    AdsInsights.Field.frequency,
    AdsInsights.Field.inline_link_clicks,
    AdsInsights.Field.cost_per_inline_link_click,
    AdsInsights.Field.ctr,
    AdsInsights.Field.cpm,
    AdsInsights.Field.cpc,
    AdsInsights.Field.clicks,
]

params = {
    'level': 'ad',
    'time_ranges': [{'since': '2022-01-01', 'until': '2099-01-01'}],
    'time_increment': 1,  # Breakdown by day
    'limit': 100
}
account = AdAccount(f"act_{ad_account_id}")
# Make the request to fetch insights
insights = account.get_insights(fields=fields, params=params)

# Iterate over the insights and print relevant data
for insight in insights:
    print('Ad Name:', insight[AdsInsights.Field.ad_name])
    print('Impressions:', insight[AdsInsights.Field.impressions])
    print('Spend:', insight[AdsInsights.Field.spend])
    print('Date Range:', insight[AdsInsights.Field.date_start], 'to', insight[AdsInsights.Field.date_stop])
    print('-------------------------')
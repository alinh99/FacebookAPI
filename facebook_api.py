from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.campaign import Campaign
import os
# Import th csv writer and the date/time function
import datetime
import csv
from dotenv import load_dotenv

load_dotenv()

#TODO: how many impressions, click on every day, month?

# Set the info to get connected to the API. Do NOT share this info
my_app_id = os.environ.get('APP_ID', '')
my_app_secret = os.environ.get('APP_SECRET', '')
my_access_token = os.environ.get('ACCESS_TOKEN', '')

# Start the connection to the facebook API
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

# Create a business object for the business account
business = Business('438409241520367')

# Get yesterday's date for the filename, and the csv data
todaybad = datetime.datetime.now()
todayslash = todaybad.strftime('%m/%d/%Y')
todayhyphen = todaybad.strftime('%m-%d-%Y')

# Define the destination filename
filename = todayhyphen + '_fb.csv'
filelocation = filename

# Get all ad accounts on the business account
accounts = business.get_owned_ad_accounts(fields=[AdAccount.Field.id])

# Open or create new file 
try:
    csvfile = open(filelocation , 'w+', encoding="utf-8", newline="")
except:
    print ("Cannot open file.")


# To keep track of rows added to file
rows = 0

try:
    # Create file writer
    filewriter = csv.writer(csvfile, delimiter=',')
except Exception as err:
    print(err)

filewriter.writerow([
    "Date of Report",
    "Account ID",
    "Account Name",
    "Ad ID",
    "Ad Name",
    "Adset ID",
    "Adset Name",
    "Campaign ID",
    "Campaign Name",
    "Spend",
    "Country",
    "Region",
    "Impressions",
    "Reach",
    # "Results"
    "Cost per results",
    "Frequency",
    "Link Clicks",
    "CTR (all)",
    "CPM (cost per 1000 impressions)",
    "CPC (all)",
    "Clicks (all)",
    "Day",
    "Delivery"
])
# Iterate through the adaccounts
start_time = datetime.datetime.now()
for account in accounts:
    # Create an addaccount object from the adaccount id to make it possible to get insights
    tempaccount = AdAccount(account[AdAccount.Field.id])

    # Grab insight info for all ads in the adaccount
    ads = tempaccount.get_insights(params={'time_range': { 'since': "2022-01-01", 'until': "2024-01-01" },
                                           'level':'ad',
                                           'limit': 100,
                                           'breakdowns': ['country', 'region'],
                                          },
                                   fields=[
                                            AdsInsights.Field.account_id,
                                            AdsInsights.Field.account_name,
                                            AdsInsights.Field.ad_id,
                                            AdsInsights.Field.ad_name,
                                            AdsInsights.Field.adset_id,
                                            AdsInsights.Field.adset_name,
                                            AdsInsights.Field.campaign_id,
                                            AdsInsights.Field.campaign_name,
                                            AdsInsights.Field.spend,
                                            AdsInsights.Field.impressions,
                                            AdsInsights.Field.reach,
                                            AdsInsights.Field.dda_results,
                                            AdsInsights.Field.cost_per_conversion,
                                            AdsInsights.Field.frequency,
                                            AdsInsights.Field.inline_link_clicks,
                                            AdsInsights.Field.ctr,
                                            AdsInsights.Field.cpm,
                                            AdsInsights.Field.cpc,
                                            AdsInsights.Field.clicks,
                                            AdsInsights.Field.date_start,
                                            AdsInsights.Field.date_stop,
                                            # AdsInsights.Field.action_values,
                                            # AdsInsights.Field.actions,
                                            # AdsInsights.Field.ad_click_actions,
                                            # AdsInsights.Field.ad_impression_actions,
                                            AdsInsights.Field.updated_time,
                                            AdsInsights.Field.created_time,
                                            AdsInsights.Field.wish_bid,
                                        ]
    )
    campaigns = tempaccount.get_campaigns(fields=[
        Campaign.Field.effective_status,
        Campaign.Field.start_time,
        Campaign.Field.id
    ])

    for campaign in campaigns:
        pass

    # Iterate through all accounts in the business account
    for ad in ads:
        # Set default values in case the insight info is empty
        date = todayslash
        accountid = ad[AdsInsights.Field.account_id]
        accountname = ""
        adid = ""
        adname = ""
        adsetid = ""
        adsetname = ""
        campaignid = ""
        campaignname = ""
        spend = ""
        country = ""
        region = ""
        impressions = ""
        reach = ""
        # dda_results = ""
        cost_per_conversion = ""
        frequency = ""
        inline_link_clicks = ""
        ctr = ""
        cpm = ""
        cpc = ""
        clicks = ""
        date_start = ""
        date_stop = ""
        delivery = ""
        day = ""
        # Set values from insight data
        if ('account_id' in ad) :
            accountid = ad[AdsInsights.Field.account_id]
        if ('account_name' in ad) :
            accountname = ad[AdsInsights.Field.account_name]
        if ('ad_id' in ad) :
            adid = ad[AdsInsights.Field.ad_id]
        if ('ad_name' in ad) :
            adname = ad[AdsInsights.Field.ad_name]
        if ('adset_id' in ad) :
            adsetid = ad[AdsInsights.Field.adset_id]
        if ('adset_name' in ad) :
            adsetname = ad[AdsInsights.Field.adset_name]
        if ('campaign_id' in ad) :
            campaignid = ad[AdsInsights.Field.campaign_id]
        if ('campaign_name' in ad) :
            campaignname = ad[AdsInsights.Field.campaign_name]

        if ('spend' in ad) :
            spend = ad[AdsInsights.Field.spend]
        if ('region' in ad) :
            region = ad['region']
        if ('country' in ad):
            country = ad['country']
        if ('impressions' in ad) :
            impressions = ad[AdsInsights.Field.impressions]
        if ('reach' in ad) :
            reach = ad[AdsInsights.Field.reach]
        if ('cost_per_conversion' in ad) :
            cost_per_conversion = ad[AdsInsights.Field.cost_per_conversion]
        if ('frequency' in ad) :
            frequency = ad[AdsInsights.Field.frequency]
        if ('inline_link_clicks' in ad) :
            inline_link_clicks = ad[AdsInsights.Field.inline_link_clicks]
        if ('ctr' in ad) :
            ctr = ad[AdsInsights.Field.ctr]
        if ('cpm' in ad) :
            cpm = ad[AdsInsights.Field.cpm]
        if ('cpc' in ad) :
            cpc = ad[AdsInsights.Field.cpc]
        if ('clicks' in ad) :
            clicks = ad[AdsInsights.Field.clicks]
        
        # if 'start_time' in campaign:
        #     if ad[AdsInsights.Field.campaign_id] == campaign[Campaign.Field.id]:
        #         day = campaign[Campaign.Field.start_time]

        # if 'effective_status' in campaign:
        #     if ad[AdsInsights.Field.campaign_id] == campaign[Campaign.Field.id]:
        #         delivery = campaign[Campaign.Field.effective_status]
        
        filewriter.writerow(
            [
                date, 
                accountid, 
                accountname, 
                adid, 
                adname, 
                adsetid, 
                adsetname, 
                campaignid, 
                campaignname, 
                spend, 
                country, 
                region,
                impressions,
                reach,
                cost_per_conversion,
                frequency,
                inline_link_clicks,
                ctr,
                cpm,
                cpc,
                clicks,
                day,
                delivery
            ]
        )
        rows += 1
        


csvfile.close()
end_time = datetime.datetime.now() - start_time
print(f"Estimated Time: {end_time}")
# Print report
print (str(rows) + " rows added to the file " + filename)
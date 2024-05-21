# Facebook Ads Manager API

## Run from Local

### Step 1:
`pip install -r requirements.txt`

### Step 2:
`pip install --upgrade 'google-cloud-bigquery[bqstorage,pandas]'`

### Step 3:
`Open the notebook file facebook_api.ipynb`

### Step 4:
`Run everything in the notebook file`

## Deploy to Google Cloud

### Step 1:
`Edit the code from the function "append_data" from main.py file`

### Step 2: Open the command line and enter the command below
`$ gcloud app deploy`

### Step 3:
`Open the link from the command: Deployed service [default] to [link/append_facebook_data] to test the deployment`
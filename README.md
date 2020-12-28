# google-data-catalog-dataprep
Update Google Cloud Data Catalog tags on BigQuery tables with Cloud Dataprep metadata and job profile

To activate and use Cloud Data Catalog you 

https://cloud.google.com/dataprep

https://cloud.google.com/functions

https://cloud.google.com/data-catalog/


This repositity contains the Cloud Function Python code to be triggered from a Dataprep Webhook to update Data Catalog tags.
https://docs.trifacta.com/display/DP/Create+Flow+Webhook+Task

In your Cloud Function, you need the 4 files:
- main.py
- config.py where you need to update your GCP project name (where Tags Template are created) and the Dataprep Access Token (to use Dataprep API)
- datacatalog_functions.py
- dataprep_metadata.py
- requirements.txt


https://console.cloud.google.com/datacatalog


This Cloud Function uses:
- Python Client for Google Cloud Data Catalog API https://googleapis.dev/python/datacatalog/latest/index.html#
- Cloud Dataprep REST API https://api.trifacta.com/dataprep-premium/index.html

To create the 2 Data Catalog Tag Template, you can use:

- gcloud
gcloud data-catalog tag-templates create - create a Cloud Data Catalog tag template
https://cloud.google.com/sdk/gcloud/reference/data-catalog/tag-templates/create
https://cloud.google.com/data-catalog/docs/quickstart-tagging#data-catalog-quickstart-gcloud

REST API
https://cloud.google.com/data-catalog/docs/quickstart-tagging#data-catalog-quickstart-drest


Happy tagging !

from google.cloud import datacatalog

datataprep_auth_token='Your Dataprep Access Token'
dataprep_headers = {"Authorization": "Bearer "+datataprep_auth_token}

dataprep_metadata_tag_template_id="cloud_dataprep_metadata"
dataprep_profile_tag_template_id="cloud_dataprep_column_profile"
dataprep_tag_template_project="Your GCP Project"

datacatalog_client = datacatalog.DataCatalogClient()
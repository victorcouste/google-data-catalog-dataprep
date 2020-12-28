# google-data-catalog-dataprep

![image](dataprep_datacatalog.png)

Update [Google Cloud Data Catalog](https://cloud.google.com/data-catalog/) tags on BigQuery tables with [Cloud Dataprep](https://cloud.google.com/dataprep) Metadata and Job profile via a [Cloud Function](https://cloud.google.com/functions).

2 Data Catalog tags are created or updated:
- **Dataprep Metadata** tag attached to the BigQuery table and containing information from Dataprep job the user, Dataprep Job (id, name, url, timestamp), Dataset (id, name, url), Flow (id, name, url), Profile (url and nb valid, invalid an empty values) and the Dataflow job (id, url).
- **Dataprep Column Profile** tag attached to each BigQuery table column and containing nb valid, invalid and empty values for the column.

To activate and use Cloud Data Catalog, go to https://cloud.google.com/data-catalog/ and https://console.cloud.google.com/datacatalog.

This repository contains the Cloud Function Python code that will be triggered from a [Dataprep Webhook](https://docs.trifacta.com/display/DP/Create+Flow+Webhook+Task) to update Data Catalog tags.

In your Cloud Function, you need the 4 files:
- **[main.py](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/main.py)**
- **[config.py](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/config.py)** where you need to update your GCP project name (where Tags Template are created) and the Dataprep Access Token (to use Dataprep API).
- **[datacatalog_functions.py](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/datacatalog_functions.py)**
- **[dataprep_metadata.py](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/dataprep_metadata.py)**
- **[requirements.txt](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/requirements.txt)**

This Cloud Function uses:
- [Python Client for Google Cloud Data Catalog API](https://googleapis.dev/python/datacatalog/latest/index.html#)
- [Cloud Dataprep REST API](https://api.trifacta.com/dataprep-premium/index.html)

To create the 2 Data Catalog Tag Template for Dataprep (Metadata and Job Profile), you can use:

- **gcloud** and the command `gcloud data-catalog tag-templates create`, details found in [gcloud_tag-templates_create.sh](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/gcloud_tag-templates_create.sh), [example](https://cloud.google.com/data-catalog/docs/quickstart-tagging#data-catalog-quickstart-gcloud) and [reference](https://cloud.google.com/sdk/gcloud/reference/data-catalog/tag-templates/create).

- **REST API** with the 2 template json files [dataprep_metadata_tag_template.json)(https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/dataprep_metadata_tag_template.json) and [dataprep_column_profile_tag_template.json](https://github.com/victorcouste/google-data-catalog-dataprep/blob/main/dataprep_column_profile_tag_template.json), [example](https://cloud.google.com/data-catalog/docs/quickstart-tagging#data-catalog-quickstart-drest) and [reference](https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.tagTemplates/create).

When Data Catalog template tags are created you can find them from https://console.cloud.google.com/datacatalog.



Happy tagging !

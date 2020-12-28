gcloud --project <your_gcp_project> data-catalog tag-templates create cloud_dataprep_metadata \
    --location=us-central1 \
    --display-name="Cloud Dataprep Metadata" \
    --field=id=dataprep_job_id,display-name="Dataprep Job ID",type=string,required=TRUE \
    --field=id=dataprep_job_timestamp,display-name="Dataprep Job Timestamp",type=timestamp,required=TRUE \
    --field=id=dataprep_user,display-name="Dataprep User",type=string,required=TRUE \
    --field=id=valid,display-name="Dataprep Job Valid values",type=double\
    --field=id=invalid,display-name="Dataprep Job Invalid values",type=double\
    --field=id=empty,display-name="Dataprep Job Empty values",type=double\
    --field=id=dataprep_job_profile,display-name="Dataprep Job Profile",type=string\
    --field=id=dataprep_job_url,display-name="Dataprep Job URL",type=string\
    --field=id=dataprep_dataset_id,display-name="Dataprep Dataset ID",type=string\
    --field=id=dataprep_dataset_name,display-name="Dataprep Dataset Name",type=string\
    --field=id=dataprep_dataset_url,display-name="Dataprep Dataset URL",type=string\
    --field=id=dataprep_flow_id,display-name="Dataprep Flow ID",type=string\
    --field=id=dataprep_flow_name,display-name="Dataprep Flow Name",type=string\
    --field=id=dataprep_flow_url,display-name="Dataprep Flow URL",type=string\
    --field=id=dataflow_job_id,display-name="Dataflow Job ID",type=string\
    --field=id=dataflow_job_url,display-name="Dataflow Job URL",type=string


gcloud --project <your_gcp_project> data-catalog tag-templates create cloud_dataprep_column_profile \
    --location=us-central1 \
    --display-name="Cloud Dataprep Column Profile" \
    --field=id=valid,display-name="Dataprep Valid values",type=double\
    --field=id=invalid,display-name="Dataprep Invalid values",type=double\
    --field=id=empty,display-name="Dataprep Empty values",type=double
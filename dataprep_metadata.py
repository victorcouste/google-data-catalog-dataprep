import requests
import json
import config

# -----------------------------------------------------------------------------------------------------------------
# ----------- FUNCTION TO GET DATAPREP METADATA FROM JOB ID ------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def get_dataprep_job(job_id):

	dataprep_job_endpoint = "https://api.clouddataprep.com/v4/jobGroups/{}?embed=wrangledDataset.recipe,wrangledDataset.flow,creator,jobs,jobs.scriptResults.storageLocation,jobgroupdataflowoptions".format(job_id)

	resp = requests.get(
	    url=dataprep_job_endpoint,
	    headers=config.dataprep_headers
	)
	job_object=resp.json()

	#print('Status Code Get Job: {}'.format(resp.status_code))
	#print('Result : {}'.format(job_object))

	for job in job_object["jobs"]["data"]:
		#print(job["jobType"])
		if job["jobType"]=="wrangle":
			dataflow_job_id = job["cpJobId"]
			for scriptResults in job["scriptResults"]["data"]:
				if scriptResults["isPrimaryOutput"]:
					output_table=scriptResults["storageLocation"]["container"]
					output_dataset=eval(scriptResults["storageLocation"]["path"])[0]

	Job_timestamp=job["updatedAt"]

	for option in job_object["jobGroupDataflowOptions"]["data"]:
		#print(option["key"])
		if option["key"]=="region":
			dataflow_location=option["value"]

	GCP_Project = job_object["wrangledDataset"]["flow"]["cpProject"]

	user = job_object["creator"]["email"]

	flow_name = job_object["wrangledDataset"]["flow"]["name"]
	flow_id = job_object["wrangledDataset"]["flow"]["id"]
	flow_url="https://clouddataprep.com/flows/{}?projectId={}".format(flow_id,GCP_Project)

	dataset_name = job_object["wrangledDataset"]["recipe"]["name"]
	dataset_id = job_object["wrangledDataset"]["id"]
	dataset_url="https://clouddataprep.com/data/{}/{}?projectId={}".format(flow_id,dataset_id,GCP_Project)

	job_url="https://clouddataprep.com/jobs/{}?projectId={}".format(job_id,GCP_Project)

	dataflow_job_url="https://console.cloud.google.com/dataflow/jobsDetail/locations/{}/jobs/{}?projectId={}".format(dataflow_location,dataflow_job_id,GCP_Project)

	job_profile="https://clouddataprep.com/v4/jobGroups/{}/pdfResults?projectId={}".format(job_id,GCP_Project)
			
	dataprep_metadata = {
		"job": {
			"dataprep_job_id": job_id, 
			"dataprep_job_timestamp": Job_timestamp,
			"dataprep_job_url": job_url,
			"dataprep_job_profile": job_profile,
			"dataprep_user": user,
			"dataprep_flow_id": str(flow_id),
			"dataprep_flow_name": flow_name,
			"dataprep_flow_url": flow_url,
			"dataprep_dataset_id": str(dataset_id),
			"dataprep_dataset_name": dataset_name,
			"dataprep_dataset_url": dataset_url,
			"dataflow_job_id":dataflow_job_id,
			"dataflow_job_url":dataflow_job_url
		},
		"output": {
			"project":GCP_Project,
			"dataset":output_dataset,
			"table":output_table
		}
	}

	return dataprep_metadata
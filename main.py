from google.cloud import datacatalog
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from config import datacatalog_client
import dataprep_metadata
import datacatalog_functions
import requests
import json
import config

def dataprep_update_datacatalog(request):

	request_json = request.get_json()
	if request_json and 'job_id' in request_json:
		dataprep_job_id = request_json['job_id']
	else:
		return 'No Dataprep Job Id for Data Catalog update'

	print('Job ID for Data Catalog tags update : {}'.format(dataprep_job_id))

	# --------------- GET DATAPREP JOB METADATA  ---------------------------------

	dataprep_job_metadata = dataprep_metadata.get_dataprep_job(dataprep_job_id)

	print('Dataprep Metadata : {}'.format(dataprep_job_metadata))

	# --------------- GET DATA CATALOG TABLE ENTRY AND TAG TEMPLATE NAMES  ---------------------------------

	dataprep_tag_templates = datacatalog_functions.get_dataprep_tag_templates()

	table_entry_name = datacatalog_functions.get_table_entry_name(dataprep_job_metadata["output"]["project"],dataprep_job_metadata["output"]["dataset"],dataprep_job_metadata["output"]["table"])

	#------------------------------------------------------------------------------------------------------------
	#------------------------------ UPDATE OR CREATE COLUMNS TAGS---------------------------------------------------
	#------------------------------------------------------------------------------------------------------------

	# --------------- GET DATAPREP JOB PROFILE RESULT  ---------------------------------

	dataprep_profile_endpoint = "https://api.clouddataprep.com/v4/jobGroups/{}/profile".format(dataprep_job_id)

	resp = requests.get(
		url=dataprep_profile_endpoint,
		headers=config.dataprep_headers
	)
	profile_object=resp.json()

	print('Job Profile Result : {}'.format(profile_object["profilerTypeCheckHistograms"]))

	columns=profile_object["profilerTypeCheckHistograms"]

	# --------------- LOOP ON DATAPREP COLUMNS ---------------------------------
	profile_nbtotal = {"VALID":0,"INVALID":0,"EMPTY":0}

	for column in columns:

		print("Tag update for Column : {}".format(column))

		datacatalog_functions.upsert_column_tag(column,columns[column],profile_nbtotal,table_entry_name,dataprep_tag_templates["profile"])

	print('Job total profile : {}'.format(profile_nbtotal))

	# -----------------------------------------------------------------------------------------------------------------
	# ------------- LIST TAGS OF TABLE ENTRY AND SEARCH IF A DATAPREP TAG EXIST -------------------
	# -----------------------------------------------------------------------------------------------

	dataprep_metadata_tag_template_found=False
	for entry_tag in datacatalog_client.list_tags(parent=table_entry_name):

		if entry_tag.template==dataprep_tag_templates["metadata"]:
			dataprep_metadata_tag_template_found=True
			dataprep_metadata_entry_tag_name=entry_tag.name
			break

	#print('Tag template found in table entry : {}'.format(dataprep_metadata_tag_template_found))

	# ----------------------------------------------------------------------------------------------------------------
	# ------------- UPDATE OR CREATE A TAG ON ENTRY TABLE ------------------------------------------------------------
	# ----------------------------------------------------------------------------------------------------------------------

	tag = datacatalog.Tag()
	dataprep_job_timestamp = Timestamp()

	# ------------- TAG CREATION FOR JOB METADATA ----------------------
	for key in dataprep_job_metadata["job"]:

		value = dataprep_job_metadata["job"][key]
		#print("The key and value are ({}) = ({})".format(key, value))
		tag_field = datacatalog.TagField()

		if key=="dataprep_job_timestamp":
			dataprep_job_timestamp.FromDatetime(datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.000Z"))
			tag_field.timestamp_value = dataprep_job_timestamp
		else:
			tag_field.string_value = value
		
		tag.fields[key] = tag_field

	# ------------- TAG CREATION FOR PROFILE RESULTS ----------------------
	for key in profile_nbtotal:
		tag_field = datacatalog.TagField()
		tag_field.double_value = profile_nbtotal[key]
		tag.fields[key] = tag_field

	if dataprep_metadata_tag_template_found:

		# ------------- UPDATE AN EXISTING TAG ON THE TABLE ENTRY----------------------
		tag.name=dataprep_metadata_entry_tag_name
		tag = datacatalog_client.update_tag(tag=tag)

	else:

		# ------------- CREATE A NEW TAG ON THE TABLE ENTRY  ----------------------
		tag.template = dataprep_tag_templates["metadata"]
		tag=datacatalog_client.create_tag(parent=table_entry_name, tag=tag)

	#print("Tag Update or Create : {}".format(tag))

	return "Data Catalog Dataprep tags updated on table {} for job {}".format(dataprep_job_metadata["output"]["table"],dataprep_job_id)